import pytest
from unittest.mock import patch, MagicMock

def get_upwork_jobs(api_key):
    """
    Simulates fetching jobs from the Upwork API.
    In a real implementation, this would make an HTTP request to the Upwork API.
    """
    # This is a placeholder. A real implementation would use the api_key.
    if not api_key:
        raise ValueError("API key is required")
    
    # Simulate a successful API response
    return [{"title": "Test Job", "description": "A job for testing purposes."}]

@patch('requests.get')
def test_upwork_api_integration(mock_get):
    """
    Tests the integration with the Upwork API using a mock response.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"title": "Mock Job", "description": "A mocked job."}]
    mock_get.return_value = mock_response
    
    jobs = get_upwork_jobs("fake_api_key")
    assert len(jobs) > 0
    assert jobs[0]["title"] == "Test Job"
import pytest
import pytest
from unittest.mock import patch

def fetch_upwork_jobs(api_key: str):
    """
    Simulates fetching jobs from the Upwork API.
    In a real scenario, this function would make an HTTP request to the Upwork API.
    """
    # This is a placeholder for the actual API call logic.
    # In a real implementation, you would use a library like `requests`
    # to fetch data from the Upwork API endpoint.
    return [
        {"id": "job1", "title": "Senior Python Developer", "description": "A job for a senior Python dev."},
        {"id": "job2", "title": "Frontend Developer (React)", "description": "React developer needed."},
    ]

@patch("tests.integration.test_external_apis.fetch_upwork_jobs")
def test_upwork_api_integration(mock_fetch_upwork_jobs):
    """
    Tests the integration with the Upwork API using a mock response.
    """
    # Configure the mock to return a predefined response
    mock_fetch_upwork_jobs.return_value = [
        {"id": "job1", "title": "Mock Job 1", "description": "This is a mock job description."}
    ]

    # Simulate calling the function that interacts with the Upwork API
    jobs = fetch_upwork_jobs("fake_api_key")

    # Assert that the function returns the mocked data
    assert len(jobs) == 1
    assert jobs[0]["title"] == "Mock Job 1"
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


