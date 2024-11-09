from fastapi import Request, Response
from typing import Callable, Optional, Dict, List
import gzip
import brotli
import zlib
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

class CompressionMiddleware:
    def __init__(
        self,
        minimum_size: int = 500,  # Minimum size in bytes to compress
        compression_level: int = 6,  # Default compression level (1-9)
        exclude_paths: set = {"/health", "/metrics"},
        exclude_types: set = {"image/", "video/", "audio/"},
        brotli_quality: int = 4,  # Brotli quality level (0-11)
        brotli_window: int = 22,  # Brotli window size (10-24)
    ):
        self.minimum_size = minimum_size
        self.compression_level = compression_level
        self.exclude_paths = exclude_paths
        self.exclude_types = exclude_types
        self.brotli_quality = brotli_quality
        self.brotli_window = brotli_window
        self.compression_stats: Dict[str, int] = {
            "gzip": 0,
            "br": 0,
            "deflate": 0,
            "uncompressed": 0
        }

    @lru_cache(maxsize=1000)
    def _should_compress(
        self,
        path: str,
        content_type: str,
        content_length: Optional[int]
    ) -> bool:
        """Determine if content should be compressed"""
        # Skip excluded paths
        if path in self.exclude_paths:
            return False

        # Skip if content type starts with any excluded type
        if any(content_type.startswith(excluded) for excluded in self.exclude_types):
            return False

        # Skip if content is too small
        if content_length and content_length < self.minimum_size:
            return False

        return True

    def _get_accepted_encodings(self, accept_encoding: str) -> List[str]:
        """Parse and sort accepted encodings by quality value"""
        if not accept_encoding:
            return []

        encodings = []
        for encoding in accept_encoding.split(","):
            encoding = encoding.strip()
            if ";q=" in encoding:
                encoding, q = encoding.split(";q=")
                q = float(q)
            else:
                q = 1.0
            encodings.append((encoding, q))

        return [e[0] for e in sorted(encodings, key=lambda x: x[1], reverse=True)]

    async def _compress_content(
        self,
        content: bytes,
        encoding: str
    ) -> Optional[bytes]:
        """Compress content using specified encoding"""
        try:
            if encoding == "br":
                compressed = brotli.compress(
                    content,
                    quality=self.brotli_quality,
                    lgwin=self.brotli_window
                )
                self.compression_stats["br"] += 1
                return compressed

            elif encoding == "gzip":
                compressed = gzip.compress(
                    content,
                    compresslevel=self.compression_level
                )
                self.compression_stats["gzip"] += 1
                return compressed

            elif encoding == "deflate":
                compressed = zlib.compress(
                    content,
                    level=self.compression_level
                )
                self.compression_stats["deflate"] += 1
                return compressed

        except Exception as e:
            logger.error(f"Compression error with {encoding}: {str(e)}")
            return None

        return None

    async def __call__(self, request: Request, call_next: Callable):
        response = await call_next(request)

        # Get response content
        response_body = await response.body()
        
        # Check if compression should be applied
        should_compress = self._should_compress(
            request.url.path,
            response.headers.get("content-type", ""),
            len(response_body)
        )

        if not should_compress:
            self.compression_stats["uncompressed"] += 1
            return response

        # Get accepted encodings
        accept_encoding = request.headers.get("accept-encoding", "")
        accepted_encodings = self._get_accepted_encodings(accept_encoding)

        # Try compression with accepted encodings
        for encoding in accepted_encodings:
            if encoding in ["br", "gzip", "deflate"]:
                compressed_content = await self._compress_content(
                    response_body,
                    encoding
                )
                
                if compressed_content:
                    # Check if compression actually helped
                    if len(compressed_content) < len(response_body):
                        headers = dict(response.headers)
                        headers["content-encoding"] = encoding
                        headers["content-length"] = str(len(compressed_content))
                        headers["vary"] = "accept-encoding"
                        
                        return Response(
                            content=compressed_content,
                            status_code=response.status_code,
                            headers=headers,
                            media_type=response.media_type
                        )

        # If no compression was applied or beneficial
        self.compression_stats["uncompressed"] += 1
        return response

    def get_compression_stats(self) -> Dict[str, int]:
        """Get compression statistics"""
        return self.compression_stats.copy()

    def reset_stats(self):
        """Reset compression statistics"""
        for key in self.compression_stats:
            self.compression_stats[key] = 0
