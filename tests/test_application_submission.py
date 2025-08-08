"""
Integration test for the ApplicationSubmissionService.
"""
import asyncio
import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from unittest.mock import AsyncMock, MagicMock

from shared.models import Job, Proposal, JobStatus, JobType
from browser_automation.application_submission_service import (
    ApplicationSubmissionService,
)
from browser_automation.director import WorkflowStatus


@pytest.fixture
def mock_director():
    """Mocks the DirectorOrchestrator."""
    mock = MagicMock()
    mock.create_workflow = AsyncMock(return_value="workflow-123")
    mock.execute_workflow = AsyncMock(
        return_value={
            "workflow_id": "workflow-123",
            "status": WorkflowStatus.COMPLETED,
            "steps": [
                {"id": "validate_proposal", "status": "completed"},
                {"id": "calculate_bid", "status": "completed"},
                {"id": "acquire_session", "status": "completed"},
                {"id": "submit_application", "status": "completed"},
                {"id": "verify_submission", "status": "completed"},
            ],
        }
    )
    return mock


@pytest.fixture
def mock_browserbase_client():
    """Mocks the BrowserbaseClient."""
    return MagicMock()


@pytest.fixture
def mock_stagehand_controller():
    """Mocks the StagehandController."""
    return MagicMock()


@pytest.fixture
def submission_service(
    mock_director, mock_browserbase_client, mock_stagehand_controller
):
    """Initializes the ApplicationSubmissionService with mocks."""
    return ApplicationSubmissionService(
        director=mock_director,
        browserbase_client=mock_browserbase_client,
        stagehand_controller=mock_stagehand_controller,
    )


@pytest.fixture
def sample_job():
    """Provides a sample job for testing."""
    return Job(
        id="job-1",
        title="Test Job",
        url="http://example.com/job/1",
        description="A test job.",
        status=JobStatus.OPEN,
        job_type=JobType.HOURLY,
    )


@pytest.fixture
def sample_proposal():
    """Provides a sample proposal for testing."""
    return Proposal(
        job_id="job-1",
        content="This is a test proposal.",
        attachments=["/path/to/resume.pdf"],
    )


@pytest.mark.asyncio
async def test_submit_application_workflow(
    submission_service, mock_director, sample_job, sample_proposal
):
    """
    Tests the full application submission workflow.
    """
    # Act
    result = await submission_service.submit_application(sample_job, sample_proposal)

    # Assert
    mock_director.create_workflow.assert_called_once()
    mock_director.execute_workflow.assert_called_once_with("workflow-123")

    assert result["status"] == WorkflowStatus.COMPLETED
    assert len(result["steps"]) == 5

    # Verify workflow definition
    create_workflow_args = mock_director.create_workflow.call_args
    steps = create_workflow_args.kwargs["steps"]

    assert steps[0]["action"] == "validate_proposals"
    assert steps[1]["action"] == "calculate_bid"
    assert steps[2]["action"] == "acquire_sessions"
    assert steps[3]["action"] == "submit_application"
    assert steps[4]["action"] == "verify_submissions"

    # Check dependencies
    assert steps[1]["dependencies"] == ["validate_proposal"]
    assert steps[2]["dependencies"] == ["calculate_bid"]
    assert steps[3]["dependencies"] == ["acquire_session"]
    assert steps[4]["dependencies"] == ["submit_application"]

    # Check parameters
    assert steps[0]["parameters"]["proposals"] == [sample_proposal.dict()]
    assert steps[3]["parameters"]["job"] == sample_job.dict()
    assert steps[3]["parameters"]["proposal"] == sample_proposal.dict()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

