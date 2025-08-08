"""
Unit tests for the GoogleService class.
"""
import unittest
from unittest.mock import MagicMock, patch

from api.services.google_services import GoogleService


class TestGoogleService(unittest.TestCase):
    """
    Test suite for the GoogleService.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        self.credentials_info = {
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
            "refresh_token": "test_refresh_token",
        }
        self.scopes = ["https://www.googleapis.com/auth/drive"]
        with patch("google.oauth2.service_account.Credentials.from_service_account_info") as mock_creds:
            self.google_service = GoogleService(self.credentials_info, self.scopes)
            self.mock_credentials = mock_creds.return_value

    @patch("googleapiclient.discovery.build")
    def test_get_drive_service(self, mock_build):
        """
        Test that the get_drive_service method returns a valid service.
        """
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        drive_service = self.google_service.get_drive_service()

        self.assertIsNotNone(drive_service)
        mock_build.assert_called_once_with("drive", "v3", credentials=self.google_service.credentials)
        self.assertEqual(drive_service, mock_service)

    @patch("googleapiclient.discovery.build")
    def test_get_docs_service(self, mock_build):
        """
        Test that the get_docs_service method returns a valid service.
        """
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        docs_service = self.google_service.get_docs_service()

        self.assertIsNotNone(docs_service)
        mock_build.assert_called_once_with("docs", "v1", credentials=self.google_service.credentials)
        self.assertEqual(docs_service, mock_service)

    @patch("googleapiclient.discovery.build")
    def test_get_sheets_service(self, mock_build):
        """
        Test that the get_sheets_service method returns a valid service.
        """
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        sheets_service = self.google_service.get_sheets_service()

        self.assertIsNotNone(sheets_service)
        mock_build.assert_called_once_with("sheets", "v4", credentials=self.google_service.credentials)
        self.assertEqual(sheets_service, mock_service)

    @patch("googleapiclient.http.MediaFileUpload")
    @patch("api.services.google_services.GoogleService.get_drive_service")
    def test_upload_file(self, mock_get_drive_service, mock_media_file_upload):
        """
        Test that the upload_file method uploads a file to Google Drive.
        """
        mock_drive_service = MagicMock()
        mock_get_drive_service.return_value = mock_drive_service
        mock_media_file_upload.return_value = MagicMock()
        mock_drive_service.files().create().execute.return_value = {"id": "test_file_id"}

        file_id = self.google_service.upload_file("test_path", "test_folder_id", "test_file_name")

        self.assertEqual(file_id, "test_file_id")

    @patch("api.services.google_services.GoogleService.get_drive_service")
    def test_create_permission(self, mock_get_drive_service):
        """
        Test that the create_permission method creates a permission for a file.
        """
        mock_drive_service = MagicMock()
        mock_get_drive_service.return_value = mock_drive_service

        self.google_service.create_permission("test_file_id", "test_email")

        mock_drive_service.permissions().create.assert_called_once()

    @patch("api.services.google_services.GoogleService.get_drive_service")
    def test_create_doc_from_template(self, mock_get_drive_service):
        """
        Test that the create_doc_from_template method creates a new Google Doc from a template.
        """
        mock_drive_service = MagicMock()
        mock_get_drive_service.return_value = mock_drive_service
        mock_drive_service.files().copy().execute.return_value = {"id": "test_doc_id"}

        doc_id = self.google_service.create_doc_from_template("test_template_id", "test_title", "test_folder_id")

        self.assertEqual(doc_id, "test_doc_id")

    @patch("api.services.google_services.GoogleService.get_docs_service")
    def test_update_doc_content(self, mock_get_docs_service):
        """
        Test that the update_doc_content method updates the content of a Google Doc.
        """
        mock_docs_service = MagicMock()
        mock_get_docs_service.return_value = mock_docs_service

        self.google_service.update_doc_content("test_doc_id", [{"test": "content"}])

        mock_docs_service.documents().batchUpdate.assert_called_once()

    @patch("api.services.google_services.GoogleService.get_sheets_service")
    @patch("api.services.google_services.GoogleService.get_drive_service")
    def test_create_spreadsheet(self, mock_get_drive_service, mock_get_sheets_service):
        """
        Test that the create_spreadsheet method creates a new Google Sheet.
        """
        mock_sheets_service = MagicMock()
        mock_get_sheets_service.return_value = mock_sheets_service
        mock_sheets_service.spreadsheets().create().execute.return_value = {"spreadsheetId": "test_sheet_id"}

        sheet_id = self.google_service.create_spreadsheet("test_title", "test_folder_id")

        self.assertEqual(sheet_id, "test_sheet_id")

    @patch("api.services.google_services.GoogleService.get_sheets_service")
    def test_append_to_sheet(self, mock_get_sheets_service):
        """
        Test that the append_to_sheet method appends data to a Google Sheet.
        """
        mock_sheets_service = MagicMock()
        mock_get_sheets_service.return_value = mock_sheets_service

        self.google_service.append_to_sheet("test_sheet_id", "test_range", [["test", "data"]])

        mock_sheets_service.spreadsheets().values().append.assert_called_once()


if __name__ == "__main__":
    unittest.main()
