# extractors/ssrs_extractor.py
import os
import requests
from requests_ntlm import HttpNtlmAuth

from etl.base.base_extractor import BaseExtractor
from config_management.factory import get_secret_manager


class SSRSExtractor(BaseExtractor):

    secret_manager = get_secret_manager()
    BASE_URL = "https://webreports.hs.uci.edu/ReportServer"

    def __init__(self):
        self.username = self.secret_manager.get_secret('ssrs_credentials', 'username')
        self.password = self.secret_manager.get_secret('ssrs_credentials', 'password')

    def connect(self):
        # For SSRS, there is no traditional "connect" step since it's more about HTTP requests
        pass

    def extract(self, parameters, output_path=None, filename=None):
        # Use default values if not provided
        output_path = output_path or os.getcwd()
        filename = filename or "outputfile.csv"

        # Construct the full URL and path for the output file
        url = self.BASE_URL + parameters
        full_path = os.path.join(output_path, filename)

        # Make a GET request with NTLM authentication
        response = requests.get(url, auth=HttpNtlmAuth(self.username, self.password))

        # Check if the request was successful
        if response.status_code == 200:
            # Save the content to a file
            with open(full_path, 'wb') as file:
                file.write(response.content)
            return full_path
        else:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

    def close(self):
        # For SSRS, there is no traditional "close" step
        pass
