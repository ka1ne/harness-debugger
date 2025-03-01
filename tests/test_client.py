"""Tests for the Harness API client."""
import unittest
from unittest.mock import patch, MagicMock
from harness_debugger.client import HarnessClient

class TestHarnessClient(unittest.TestCase):
    def setUp(self):
        # Set up test environment
        self.client = HarnessClient(
            api_key="test_api_key",
            account_id="test_account_id"
        )
    
    @patch('harness_debugger.client.requests.get')
    def test_get_delegate_info(self, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "SUCCESS",
            "data": {
                "uuid": "test-delegate-id",
                "name": "test-delegate",
                # Add other fields as needed
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.client.get_delegate_info("test-delegate-id")
        
        # Assert the result
        self.assertEqual(result.get("id"), "test-delegate-id")
        self.assertEqual(result.get("name"), "test-delegate")
        
    # Add more tests for other methods

if __name__ == '__main__':
    unittest.main() 