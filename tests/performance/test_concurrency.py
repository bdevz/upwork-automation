import pytest
import asyncio

async def simulate_user_session(session_id):
    """
    Simulates a user session performing a series of actions.
    """
    print(f"Starting session {session_id}")
    await asyncio.sleep(0.1)  # Simulate work
    print(f"Finishing session {session_id}")
    return f"Session {session_id} completed"

@pytest.mark.asyncio
async def test_concurrent_sessions(benchmark):
    """
    Tests the system's ability to handle multiple concurrent user sessions.
    This test uses pytest-benchmark to measure performance.
    """
    async def run_sessions():
        tasks = [simulate_user_session(i) for i in range(10)]
        await asyncio.gather(*tasks)

    benchmark(run_sessions)
