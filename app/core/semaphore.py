import asyncio
from app.config import settings


class SemaphoreManager:
    """Manages global and internal semaphores for concurrency control"""

    def __init__(self):
        # Global Semaphore: Limits concurrent repository processing (1-2)
        # Prevents OOM from git clone and parsing operations
        self.global_semaphore = asyncio.Semaphore(settings.global_semaphore_limit)

        # Internal Semaphore: Limits concurrent AI chunk requests (10)
        # Maximizes speed during Map phase by parallelizing I/O-bound API calls
        self.internal_semaphore = asyncio.Semaphore(settings.internal_semaphore_limit)

    async def acquire_global(self):
        """Acquire global semaphore for repository-level processing"""
        await self.global_semaphore.acquire()

    def release_global(self):
        """Release global semaphore"""
        self.global_semaphore.release()

    async def acquire_internal(self):
        """Acquire internal semaphore for chunk-level AI requests"""
        await self.internal_semaphore.acquire()

    def release_internal(self):
        """Release internal semaphore"""
        self.internal_semaphore.release()


# Global semaphore manager instance
semaphore_manager = SemaphoreManager()
