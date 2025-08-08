"""
Integration tests for the n8n webhooks API.
"""
import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
import uuid

from api.main import app


@pytest.fixture
def director_orchestrator_mock():
    """Mocks the DirectorOrchestrator to prevent actual browser automation."""
    with patch("api.routers.n8n_webhooks.DirectorOrchestrator") as mock_class:
        mock_instance = AsyncMock()
        mock_class.create.return_value = mock_instance
        yield mock_instance


@pytest.mark.asyncio
async def test_trigger_job_discovery(director_orchestrator_mock):
    """Test the /job-discovery endpoint."""
    with patch(
        "api.routers.n8n_webhooks.create_job_discovery_workflow", new_callable=AsyncMock
    ) as mock_workflow:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                "/api/n8n/job-discovery",
                json={"keywords": ["Salesforce", "Developer"]},
            )
        assert response.status_code == 200
        assert response.json() == {
            "message": "Job discovery workflow triggered successfully"
        }
        director_orchestrator_mock.create.assert_called_once()
        mock_workflow.assert_called_once_with(
            await director_orchestrator_mock.create(),
            keywords=["Salesforce", "Developer"],
            parallel=True,
        )


@pytest.mark.asyncio
async def test_trigger_proposal_generation(director_orchestrator_mock):
    """Test the /generate-proposal endpoint."""
    job_id = str(uuid.uuid4())
    with patch(
        "api.routers.n8n_webhooks.create_proposal_generation_workflow",
        new_callable=AsyncMock,
    ) as mock_workflow:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                "/api/n8n/generate-proposal",
                json={"job_id": job_id, "custom_instructions": "Test instructions"},
            )
        assert response.status_code == 200
        assert response.json() == {
            "message": "Proposal generation workflow triggered successfully"
        }
        mock_workflow.assert_called_once()


@pytest.mark.asyncio
async def test_trigger_application_submission(director_orchestrator_mock):
    """Test the /submit-application endpoint."""
    job_id = str(uuid.uuid4())
    proposal_id = str(uuid.uuid4())
    with patch(
        "api.routers.n8n_webhooks.create_proposal_submission_workflow",
        new_callable=AsyncMock,
    ) as mock_workflow:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                "/api/n8n/submit-application",
                json={"job_id": job_id, "proposal_id": proposal_id},
            )
        assert response.status_code == 200
        assert response.json() == {
            "message": "Application submission workflow triggered successfully"
        }
        mock_workflow.assert_called_once()


@pytest.mark.asyncio
@patch("api.routers.n8n_webhooks.send_slack_notification", new_callable=AsyncMock)
async def test_notify(send_slack_notification_mock):
    """Test the /notify endpoint."""
