from fastapi import Request, Response
from typing import Callable, Dict, Optional
import logging
import time
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

class DatabaseMiddleware:
    def __init__(
        self,
        database_url: str,
        pool_size: int = 20,
        max_overflow: int = 10,
        pool_timeout: int = 30,
        pool_recycle: int = 1800,
        echo: bool = False,
        stats_enabled: bool = True
    ):
        self.database_url = database_url
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_timeout = pool_timeout
        self.pool_recycle = pool_recycle
        self.echo = echo
        self.stats_enabled = stats_enabled
        
        # Initialize statistics
        self.stats = {
            "total_connections": 0,
            "active_connections": 0,
            "errors": 0,
            "slow_queries": 0,
            "query_times": []
        }
        
        # Initialize engine and session factory
        self._initialize_engine()

    def _initialize_engine(self):
        """Initialize database engine and session factory"""
        self.engine = create_async_engine(
            self.database_url,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            pool_timeout=self.pool_timeout,
            pool_recycle=self.pool_recycle,
            echo=self.echo
        )
        
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        """Get database session with automatic cleanup"""
        session = self.session_factory()
        start_time = time.time()
        
        try:
            if self.stats_enabled:
                self.stats["total_connections"] += 1
                self.stats["active_connections"] += 1
            
            yield session
            
            await session.commit()
            
        except SQLAlchemyError as e:
            await session.rollback()
            if self.stats_enabled:
                self.stats["errors"] += 1
            logger.error(f"Database error: {str(e)}")
            raise
        
        finally:
            await session.close()
            if self.stats_enabled:
                self.stats["active_connections"] -= 1
                query_time = time.time() - start_time
                self.stats["query_times"].append(query_time)
                if query_time > 1.0:  # Slow query threshold: 1 second
                    self.stats["slow_queries"] += 1
                # Keep only last 1000 query times
                if len(self.stats["query_times"]) > 1000:
                    self.stats["query_times"] = self.stats["query_times"][-1000:]

    async def cleanup(self):
        """Cleanup database connections"""
        if self.engine:
            await self.engine.dispose()

    async def health_check(self) -> bool:
        """Check database connectivity"""
        try:
            async with self.get_session() as session:
                await session.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return False

    def get_stats(self) -> Dict:
        """Get database connection statistics"""
        if not self.stats_enabled:
            return {"stats_enabled": False}
            
        query_times = self.stats["query_times"]
        avg_query_time = sum(query_times) / len(query_times) if query_times else 0
        
        return {
            "total_connections": self.stats["total_connections"],
            "active_connections": self.stats["active_connections"],
            "errors": self.stats["errors"],
            "slow_queries": self.stats["slow_queries"],
            "average_query_time": avg_query_time,
            "pool_size": self.pool_size,
            "max_overflow": self.max_overflow
        }

    async def __call__(self, request: Request, call_next: Callable):
        # Add database session to request state
        async with self.get_session() as session:
            request.state.db = session
            
            try:
                response = await call_next(request)
                return response
                
            except Exception as e:
                logger.error(f"Request error with database session: {str(e)}")
                raise
                
            finally:
                # Remove database session from request state
                if hasattr(request.state, "db"):
                    delattr(request.state, "db")

class AsyncDatabaseSession:
    """Async database session context manager for use in routes"""
    
    def __init__(self, request: Request):
        self.request = request

    async def __aenter__(self) -> AsyncSession:
        if not hasattr(self.request.state, "db"):
            raise RuntimeError("Database session not available in request state")
        return self.request.state.db

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

# Helper function to get database session in routes
async def get_db(request: Request) -> AsyncSession:
    async with AsyncDatabaseSession(request) as session:
        return session
