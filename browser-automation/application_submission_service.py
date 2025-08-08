from typing import Any, Dict, List, Optional
from browser_automation.director import DirectorOrchestrator
from browser_automation.session_manager import SessionManager
from browser_automation.stagehand_controller import StagehandController
from browser_automation.browserbase_client import BrowserbaseClient
from shared.utils import setup_logging

logger = setup_logging("application_submission_service")


class ApplicationSubmissionService:
    """
    Service to manage the application submission workflow.
    """

    def __init__(
        self,
        director: DirectorOrchestrator,
        session_manager: SessionManager,
        stagehand_controller: StagehandController,
        browserbase_client: BrowserbaseClient,
    ):
        self.director = director
        self.session_manager = session_manager
        self.stagehand_controller = stagehand_controller
        self.browserbase_client = browserbase_client

    async def submit_application_workflow(
        self, application_data: Dict[str, Any]
    ) -> str:
        """
        Create and execute a workflow for submitting a single application.

        Args:
            application_data: A dictionary containing the application details.

        Returns:
            The ID of the executed workflow.
        """
        steps = [
            {
                "id": "validate_application",
                "name": "Validate Application Data",
                "action": "validate_proposals",
                "parameters": {"proposals": [application_data]},
            },
            {
                "id": "calculate_bid",
                "name": "Calculate Bid Amount",
                "action": "calculate_bid",
                "parameters": {"job_details": application_data.get("job_details", {})},
                "dependencies": ["validate_application"],
            },
            {
                "id": "acquire_session",
                "name": "Acquire Submission Session",
                "action": "acquire_sessions",
                "parameters": {"session_type": "proposal_submission", "count": 1},
                "dependencies": ["calculate_bid"],
            },
            {
                "id": "submit_application",
                "name": "Submit Application",
                "action": "submit_application",
                "parameters": {"application_data": application_data},
                "dependencies": ["acquire_session"],
            },
            {
                "id": "verify_submission",
                "name": "Verify Submission",
                "action": "verify_submissions",
                "parameters": {},
                "dependencies": ["submit_application"],
            },
        ]

        workflow_id = await self.director.create_workflow(
            name="Single Application Submission",
            description=f"Submit application for job: {application_data.get('job_title', 'N/A')}",
            steps=steps,
            parallel_execution=False,
            session_requirements={
                "min_sessions": 1,
                "session_type": "proposal_submission",
            },
        )

        return await self.director.execute_workflow(workflow_id)

