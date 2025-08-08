"""
Service for interacting with Google Workspace APIs (Docs and Drive).
"""
import json
from typing import Dict, List

from google.oauth2 import service_account
from googleapiclient.discovery import build

from shared.config import settings
from shared.utils import setup_logging

logger = setup_logging("google_services")

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
]


def get_google_credentials():
    """
    Loads Google credentials from the configuration.
    """
    if not settings.google_credentials:
        raise ValueError("Google credentials are not configured.")
    
    creds_json = json.loads(settings.google_credentials)
    return service_account.Credentials.from_service_account_info(creds_json, scopes=SCOPES)


async def create_proposal_doc(title: str, content: str) -> Dict[str, str]:
    """
    Creates a new Google Doc with the proposal content.
    """
    credentials = get_google_credentials()
    docs_service = build("docs", "v1", credentials=credentials)

    document = {
        "title": title,
        "body": {"content": [{"paragraph": {"elements": [{"textRun": {"content": content}}]}}]},
    }

    try:
        doc = docs_service.documents().create(body=document).execute()
        doc_id = doc.get("documentId")
        return {
            "google_doc_id": doc_id,
            "google_doc_url": f"https://docs.google.com/document/d/{doc_id}/edit",
        }
    except Exception as e:
        logger.error(f"Error creating Google Doc: {e}")
        return {}


async def find_relevant_attachments(job_description: str) -> List[str]:
    """
    Finds relevant attachments from a Google Drive folder based on job description keywords.
    """
    credentials = get_google_credentials()
    drive_service = build("drive", "v3", credentials=credentials)
    folder_id = settings.google_drive_folder_id

    if not folder_id:
        logger.warning("Google Drive folder ID is not configured.")
        return []

    try:
        # This is a placeholder for a more sophisticated keyword matching implementation
        return ["drive_file_id_1", "drive_file_id_2"]
    except Exception as e:
        logger.error(f"Error searching for attachments in Google Drive: {e}")
        return []

