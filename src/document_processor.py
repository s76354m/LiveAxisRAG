from typing import List
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from .config import Config
import logging
import os
import hashlib
from tqdm import tqdm

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        self.embedding_model = OpenAIEmbeddings(
            model="text-embedding-3-large",
            dimensions=1536
        )
        self.cache_dir = "cache"
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def get_cache_path(self, pdf_path: str) -> str:
        """Generate cache file path based on PDF hash"""
        pdf_hash = hashlib.md5(open(pdf_path, 'rb').read()).hexdigest()
        return os.path.join(self.cache_dir, f"{pdf_hash}.faiss")
        
    def process_document(self, pdf_path: str):
        """Process document with caching"""
        cache_path = self.get_cache_path(pdf_path)
        
        if os.path.exists(cache_path):
            logger.info("Loading cached vector store...")
            try:
                return FAISS.load_local(
                    folder_path=cache_path, 
                    embeddings=self.embedding_model,
                    allow_dangerous_deserialization=True  # Only for local, trusted files
                )
            except Exception as e:
                logger.warning(f"Cache load failed, reprocessing document: {str(e)}")
                # If cache load fails, remove corrupt cache and reprocess
                try:
                    os.remove(cache_path)
                except:
                    pass
            
        try:
            text = self.extract_text_from_pdf(pdf_path)
            chunks = self.split_text(text)
            
            # Batch process embeddings
            logger.info("Creating embeddings in batches...")
            batch_size = 100
            vector_store = None
            
            with tqdm(total=len(chunks)) as pbar:
                for i in range(0, len(chunks), batch_size):
                    batch = chunks[i:i + batch_size]
                    if vector_store is None:
                        vector_store = FAISS.from_texts(
                            texts=batch,
                            embedding=self.embedding_model
                        )
                    else:
                        vector_store.add_texts(batch)
                    pbar.update(len(batch))
            
            # Cache the vector store
            vector_store.save_local(cache_path)
            logger.info("Vector store cached successfully")
            
            return vector_store
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file with page limit consideration"""
        text = ""
        max_pages = Config.get_max_pages()
        
        try:
            doc = fitz.open(pdf_path)
            total_pages = min(len(doc), max_pages)
            
            for page_num in range(total_pages):
                if page_num % 5 == 0:  # Log progress every 5 pages
                    logger.info(f"Processed {page_num}/{total_pages} pages...")
                
                page = doc[page_num]
                text += page.get_text()
            
            logger.info("PDF extraction complete")
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise

    def split_text(self, text: str) -> List[str]:
        """Split text into chunks"""
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=Config.CHUNK_SIZE,
                chunk_overlap=Config.CHUNK_OVERLAP,
                length_function=len,
            )
            
            chunks = text_splitter.split_text(text)
            logger.info(f"Created {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Error splitting text: {str(e)}")
            raise
