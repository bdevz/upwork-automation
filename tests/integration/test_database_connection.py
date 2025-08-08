import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import os

# Define the test database URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://ardan_user:ardan_pass@localhost:5432/ardan_automation")

@pytest_asyncio.fixture(scope="module")
async def async_engine():
    """Create an async engine for the tests."""
    engine = create_async_engine(DATABASE_URL, echo=True)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def db_session(async_engine):
    """Create a new database session for each test."""
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

@pytest.mark.asyncio
async def test_database_connection(db_session: AsyncSession):
    """
    Tests the basic database connection and query execution.
    """
    try:
        # Execute a simple query to check the connection
        result = await db_session.execute(text("SELECT 1"))
        assert result.scalar_one() == 1, "Database connection check failed"
    except Exception as e:
        pytest.fail(f"Database connection failed with an exception: {e}")

@pytest.mark.asyncio
async def test_crud_operations(db_session: AsyncSession):
    """
    Placeholder for CRUD operations test.
    This test will be expanded to cover create, read, update, and delete operations.
    """
    # This is a placeholder test.
    # In a real-world scenario, you would use your application's models to
    # create a test record, read it, update it, and then delete it.
    # For now, we'll just assert that the test passes.
    assert True

