"""
Service for interacting with Google APIs (Drive, Docs, Sheets).
"""
import logging
from typing import Any, Dict, List, Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build, Resource
from googleapiclient import http
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
        if not self.sheets_service:
            self.sheets_service = self._build_service("sheets", "v4")
        return self.sheets_service

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def upload_file(self, file_path: str, folder_id: str, file_name: Optional[str] = None) -> Optional[str]:
        """
        Uploads a file to a specified Google Drive folder.

        Args:
            file_path (str): The local path to the file.
            folder_id (str): The ID of the Google Drive folder.
            file_name (str, optional): The name to save the file as. Defaults to the original file name.

        Returns:
            Optional[str]: The ID of the uploaded file, or None if the upload fails.
        """
        try:
            drive_service = self.get_drive_service()
            file_metadata = {"name": file_name or file_path.split("/")[-1], "parents": [folder_id]}
            media = http.MediaFileUpload(file_path, resumable=True)
            file = (
                drive_service.files()
                .create(body=file_metadata, media_body=media, fields="id")
                .execute()
            )
            logger.info(f"File '{file_name}' uploaded with ID: {file.get('id')}")
            return file.get("id")
        except Exception as e:
            logger.error(f"Failed to upload file to Google Drive: {e}")
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def create_permission(self, file_id: str, email_address: str, role: str = "reader"):
        """
        Creates a permission for a file on Google Drive.

        Args:
            file_id (str): The ID of the file.
            email_address (str): The email address to grant permission to.
            role (str): The role to grant (e.g., 'reader', 'writer', 'commenter').
        """
        try:
            drive_service = self.get_drive_service()
            permission = {"type": "user", "role": role, "emailAddress": email_address}
            drive_service.permissions().create(fileId=file_id, body=permission).execute()
            logger.info(f"Permission granted to {email_address} for file {file_id}")
        except Exception as e:
            logger.error(f"Failed to create permission for file {file_id}: {e}")

    def get_google_drive_folder_id(self) -> Optional[str]:
        """Returns the Google Drive folder ID from settings."""
        return settings.google_drive_folder_id

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def create_doc_from_template(self, template_id: str, title: str, folder_id: str) -> Optional[str]:
        """
        Creates a new Google Doc from a template.

        Args:
            template_id (str): The ID of the template document.
            title (str): The title of the new document.
            folder_id (str): The ID of the folder to create the document in.

        Returns:
            Optional[str]: The ID of the new document, or None if creation fails.
        """
        try:
            drive_service = self.get_drive_service()
            body = {"name": title, "parents": [folder_id]}
            doc = drive_service.files().copy(fileId=template_id, body=body).execute()
            logger.info(f"Document '{title}' created with ID: {doc.get('id')}")
            return doc.get("id")
        except Exception as e:
            logger.error(f"Failed to create document from template: {e}")
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def update_doc_content(self, doc_id: str, content: List[Dict[str, Any]]):
        """
        Updates the content of a Google Doc.

        Args:
            doc_id (str): The ID of the document to update.
            content (List[Dict[str, Any]]): A list of requests to update the document.
        """
        try:
            docs_service = self.get_docs_service()
            docs_service.documents().batchUpdate(documentId=doc_id, body={"requests": content}).execute()
            logger.info(f"Document {doc_id} updated successfully.")
        except Exception as e:
            logger.error(f"Failed to update document {doc_id}: {e}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def create_spreadsheet(self, title: str, folder_id: str) -> Optional[str]:
        """
        Creates a new Google Sheet.

        Args:
            title (str): The title of the new spreadsheet.
            folder_id (str): The ID of the Google Drive folder to create the sheet in.

        Returns:
            Optional[str]: The ID of the new spreadsheet, or None if creation fails.
        """
        try:
            sheets_service = self.get_sheets_service()
            spreadsheet = {"properties": {"title": title}}
            sheet = (
                sheets_service.spreadsheets()
                .create(body=spreadsheet, fields="spreadsheetId")
                .execute()
            )
            sheet_id = sheet.get("spreadsheetId")
            drive_service = self.get_drive_service()
            drive_service.files().update(
                fileId=sheet_id, addParents=folder_id, removeParents="root"
            ).execute()
            logger.info(f"Spreadsheet '{title}' created with ID: {sheet_id}")
            return sheet_id
        except Exception as e:
            logger.error(f"Failed to create spreadsheet: {e}")
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def append_to_sheet(self, spreadsheet_id: str, range_name: str, values: List[List[Any]]):
        """
        Appends data to a Google Sheet.

