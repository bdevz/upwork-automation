"""
Utility functions for the Ardan Automation System
"""
from typing import Any, Coroutine
import asyncio
from functools import wraps
from shared.logger import logger


def retry_async(
    retries: int = 3, delay: int = 1, backoff: int = 2
) -> Coroutine[Any, Any, Any]:
    """
    Decorator for retrying async functions with exponential backoff.
    """

    def decorator(func: Coroutine[Any, Any, Any]) -> Coroutine[Any, Any, Any]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_delay = delay
            for i in range(retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if i == retries - 1:
                        logger.error(f"Function {func.__name__} failed after {retries} retries.")
                        raise
                    logger.warning(
                        f"Function {func.__name__} failed. Retrying in {current_delay} seconds..."
                    )
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator
