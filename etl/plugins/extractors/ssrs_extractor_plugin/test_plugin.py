import unittest
from unittest.mock import patch, Mock, ANY

from .plugin import SSRSExtractor


class TestSSRSExtractor(unittest.TestCase):

    @patch('etl.plugins.extractors.ssrs_extractor_plugin.plugin.get_secret_manager')
    @patch('etl.plugins.extractors.ssrs_extractor_plugin.plugin.requests.get')
    def test_extract_successful_response(self, mock_get, mock_get_secret_manager):
        # Mock secret manager responses
        mock_secret_manager = Mock()
        mock_secret_manager.get_secret.side_effect = ['mock_username', 'mock_password']
        mock_get_secret_manager.return_value = mock_secret_manager

        # Mock a successful response from the SSRS server
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"mock_data"
        mock_get.return_value = mock_response

        extractor = SSRSExtractor()
        output_path = extractor.extract("/mock_report_path")

        # Assertions
        mock_get.assert_called_with(
            "https://webreports.hs.uci.edu/ReportServer/mock_report_path", 
            auth=ANY  # Placeholder for expected auth object
        )
        self.assertTrue("outputfile.csv" in output_path)

    # TODO: Additional tests, e.g., for unsuccessful HTTP responses, exceptions, etc.

if __name__ == '__main__':
    unittest.main()
