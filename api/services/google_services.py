"""
Service for interacting with Google APIs (Drive, Docs, Sheets).
"""
import logging
from typing import Any, Dict, List, Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build, Resource
from tenacity import retry, stop_after_attempt, wait_exponential

from shared.config import settings

logger = logging.getLogger(__name__)


class GoogleService:
    """
    A service class for handling interactions with Google services like Drive, Docs, and Sheets.
    """

    def __init__(self, credentials_info: Dict[str, Any], scopes: List[str]):
        """
        Initializes the GoogleService with service account credentials.

        Args:
            credentials_info (Dict[str, Any]): The service account credentials.
            scopes (List[str]): The list of scopes for Google APIs.
        """
        self.credentials = service_account.Credentials.from_service_account_info(
            credentials_info, scopes=scopes
        )
        self.drive_service: Optional[Resource] = None
        self.docs_service: Optional[Resource] = None
        self.sheets_service: Optional[Resource] = None

    def _build_service(self, service_name: str, version: str) -> Resource:
        """Builds a Google API service resource."""
        return build(service_name, version, credentials=self.credentials)

    def get_drive_service(self) -> Resource:
        """Returns a Google Drive API service."""
        if not self.drive_service:
            self.drive_service = self._build_service("drive", "v3")
        return self.drive_service

    def get_docs_service(self) -> Resource:
        """Returns a Google Docs API service."""
        if not self.docs_service:
            self.docs_service = self._build_service("docs", "v1")
        return self.docs_service

    def get_sheets_service(self) -> Resource:
        """Returns a Google Sheets API service."""
