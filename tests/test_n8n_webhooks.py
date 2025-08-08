import pytest
from unittest.mock import AsyncMock, patch

from httpx import AsyncClient
from fastapi import status
from main import app


@pytest.mark.asyncio
@patch("api.routers.n8n_webhooks.DirectorOrchestrator")
async def test_trigger_job_discovery(mock_director_orchestrator):
    """Test the job discovery webhook endpoint."""
    mock_director = AsyncMock()
    mock_director_orchestrator.create.return_value = mock_director

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/n8n/job-discovery",
            json={"keywords": ["Salesforce", "Developer"]},
        )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Job discovery workflow triggered successfully"}
    mock_director_orchestrator.create.assert_called_once()


@pytest.mark.asyncio
@patch("api.routers.n8n_webhooks.DirectorOrchestrator")
async def test_trigger_proposal_generation(mock_director_orchestrator):
    """Test the proposal generation webhook endpoint."""
    mock_director = AsyncMock()
    mock_director_orchestrator.create.return_value = mock_director

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/n8n/generate-proposal",
            json={
                "job_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                "custom_instructions": "Focus on my AI experience.",
            },
        )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "Proposal generation workflow triggered successfully"
    }
    mock_director_orchestrator.create.assert_called_once()


@pytest.mark.asyncio
@patch("api.routers.n8n_webhooks.DirectorOrchestrator")
async def test_trigger_application_submission(mock_director_orchestrator):
    """Test the application submission webhook endpoint."""
    mock_director = AsyncMock()
    mock_director_orchestrator.create.return_value = mock_director

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/n8n/submit-application",
            json={
                "job_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                "proposal_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12",
            },
        )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "Application submission workflow triggered successfully"
    }
    mock_director_orchestrator.create.assert_called_once()


@pytest.mark.asyncio
@patch("api.routers.n8n_webhooks.send_slack_notification")
async def test_send_notification(mock_send_slack_notification):
    """Test the notification webhook endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/n8n/notify", params={"message": "Test notification"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Notification sent successfully"}
    mock_send_slack_notification.assert_called_once_with("Test notification")
