
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


if __name__ == "__main__":
    unittest.main()
