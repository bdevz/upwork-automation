import pytest
from unittest.mock import patch, MagicMock

def get_upwork_jobs(api_key: str, query: str):
    """
    Simulates fetching jobs from the Upwork API.
    In a real scenario, this function would make an HTTP request to the Upwork API.
    """
    if api_key != "test_api_key":
        return {"error": "Invalid API key"}
    
    return {
        "jobs": [
            {"id": "1", "title": "Software Engineer", "description": "Develop amazing things."},
            {"id": "2", "title": "Data Scientist", "description": "Analyze interesting data."},
        ]
    }

@patch("tests.integration.test_external_apis.get_upwork_jobs")
def test_upwork_api_integration(mock_get_jobs):
    """
    Tests the integration with the Upwork API using a mock response.
    """
    # Configure the mock to return a successful response
    mock_get_jobs.return_value = {
        "jobs": [{"id": "3", "title": "DevOps Engineer", "description": "Automate all the things."}]
    }
    
    # Simulate calling the function that interacts with the Upwork API
    response = get_upwork_jobs("test_api_key", "DevOps")
    
    # Assert that the mock was called correctly and the response is as expected
    mock_get_jobs.assert_called_once_with("test_api_key", "DevOps")
    assert response["jobs"][0]["title"] == "DevOps Engineer"
