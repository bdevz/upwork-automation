import asyncio
import time
import pytest
from shared.utils import AsyncRateLimiter

@pytest.mark.asyncio
async def test_async_rate_limiter_wait():
    """Test that the rate limiter waits for the correct amount of time."""
    rate_limiter = AsyncRateLimiter(rate_limit=10)  # 10 calls per second
    start_time = time.monotonic()
    for _ in range(5):
        await rate_limiter.wait()
    end_time = time.monotonic()
    duration = end_time - start_time
    assert duration >= 0.4  # 4 * 0.1 seconds

@pytest.mark.asyncio
async def test_async_rate_limiter_no_wait():
    """Test that the rate limiter does not wait if the rate is not exceeded."""
    rate_limiter = AsyncRateLimiter(rate_limit=1)  # 1 call per second
    start_time = time.monotonic()
    await rate_limiter.wait()
    await asyncio.sleep(1.1)
    await rate_limiter.wait()
    end_time = time.monotonic()
    duration = end_time - start_time
    assert duration < 1.2

@pytest.mark.asyncio
async def test_async_rate_limiter_jitter():
    """Test that the rate limiter applies jitter to the wait time."""
    rate_limiter = AsyncRateLimiter(rate_limit=10, jitter=0.5)
    start_time = time.monotonic()
    for _ in range(10):
        await rate_limiter.wait()
    end_time = time.monotonic()
    duration = end_time - start_time
    # With 50% jitter, the total time should be around 0.9s, but could be more or less
    # We'll check that it's within a reasonable range
    assert 0.8 < duration < 1.5

@pytest.mark.asyncio
async def test_async_rate_limiter_update_rate():
    """Test that the rate limit can be updated dynamically."""
    rate_limiter = AsyncRateLimiter(rate_limit=1)  # 1 call per second
    start_time = time.monotonic()
    await rate_limiter.wait()
    rate_limiter.update_rate_limit(10)  # 10 calls per second
    for _ in range(5):
        await rate_limiter.wait()
    end_time = time.monotonic()
    duration = end_time - start_time
    assert duration < 1.0  # Should be much faster than 5 seconds
