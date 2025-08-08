import pytest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api.main import app
from database.connection import get_db
from shared.models import Base, Job, Proposal

# Setup the in-memory SQLite database for testing
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


@pytest.fixture(scope="module")
async def test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def db_session():
    return TestingSessionLocal()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.mark.unit
@patch("api.services.proposal_generator.client", new_callable=AsyncMock)
async def test_generate_proposal_content(mock_openai_client):
    from api.services.proposal_generator import generate_proposal_content

    mock_openai_client.chat.completions.create.return_value.choices[0].message.content = "Test proposal"
    job = Job(title="Test Job", description="Test Description")
    content = await generate_proposal_content(job)
    assert content == "Test proposal"


@pytest.mark.unit
@patch("api.services.google_services.build")
async def test_create_proposal_doc(mock_build):
    from api.services.google_services import create_proposal_doc

    mock_docs_service = mock_build.return_value
    mock_docs_service.documents().create().execute.return_value = {
        "documentId": "test_doc_id"
    }
    result = await create_proposal_doc("Test Title", "Test Content")
    assert result["google_doc_id"] == "test_doc_id"


@pytest.mark.integration
@patch("api.services.proposal_generator.generate_proposal_content", new_callable=AsyncMock)
@patch("api.services.proposal_generator.score_proposal_quality", new_callable=AsyncMock)
@patch("api.services.google_services.create_proposal_doc", new_callable=AsyncMock)
@patch("api.services.google_services.find_relevant_attachments", new_callable=AsyncMock)
async def test_generate_proposal_endpoint(
    mock_find_attachments,
    mock_create_doc,
    mock_score_proposal,
    mock_generate_content,
    client,
    db_session,
    test_db,
):
    # Mock service responses
    mock_generate_content.return_value = "Generated proposal content."
    mock_score_proposal.return_value = {
        "quality_score": 0.9,
        "optimization_suggestions": ["Looks good."],
    }
    mock_create_doc.return_value = {
        "google_doc_id": "fake_doc_id",
        "google_doc_url": "http://fake.doc/url",
    }
    mock_find_attachments.return_value = ["fake_attachment_id"]

    # Create a job to generate a proposal for
    job = Job(
        title="Software Engineer",
        description="Develop amazing things.",
        client_rating=4.5,
        client_payment_verified=True,
        client_hire_rate=0.8,
        job_type="hourly",
    )
    db_session.add(job)
    await db_session.commit()
    await db_session.refresh(job)

    # Make the API request
    response = client.post(
        "/api/proposals/generate",
        json={"job_id": str(job.id), "include_attachments": True},
    )

    # Assertions
    assert response.status_code == 200
    proposal_data = response.json()
    assert proposal_data["job_id"] == str(job.id)
    assert proposal_data["content"] == "Generated proposal content."
    assert proposal_data["quality_score"] == 0.9
    assert proposal_data["google_doc_id"] == "fake_doc_id"
    assert proposal_data["attachments"] == ["fake_attachment_id"]

    # Verify the proposal was saved to the database
    proposal = await db_session.get(Proposal, proposal_data["id"])
    assert proposal is not None
    assert proposal.quality_score == 0.9

