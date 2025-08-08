import pytest
from unittest.mock import MagicMock

# Mock for a browser automation framework like Selenium or Playwright
class MockBrowser:
    def __init__(self):
        self.page_content = ""

    def navigate(self, url):
        """Simulates navigating to a URL."""
        if "login.html" in url:
            with open("tests/ui/mock_pages/login.html", "r") as f:
                self.page_content = f.read()
        elif "job_post.html" in url:
            with open("tests/ui/mock_pages/job_post.html", "r") as f:
                self.page_content = f.read()

    def click(self, selector):
        """Simulates clicking an element."""
        # In a real test, this would interact with the browser
        print(f"Clicked on element: {selector}")

    def get_page_source(self):
        """Returns the current page source."""
        return self.page_content

def test_browser_login_and_apply():
    """
    Tests a simplified user workflow: logging in and applying for a job.
    """
    browser = MockBrowser()

    # 1. Simulate logging in
    browser.navigate("tests/ui/mock_pages/login.html")
    assert "<h1>Login</h1>" in browser.get_page_source()

    # 2. Navigate to a job post and simulate applying
    browser.navigate("tests/ui/mock_pages/job_post.html")
