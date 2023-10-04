# extractors/ssrs_extractor.py
import os
import requests
import yaml
from requests_ntlm import HttpNtlmAuth
from urllib.parse import quote

from etl.base.base_extractor import BaseExtractor
from config_management.factory import get_secret_manager


class SSRSExtractor(BaseExtractor):

    secret_manager = get_secret_manager()

    def __init__(self):
        domain = self.secret_manager.get_secret('ssrs_credentials', 'domain')
        username = self.secret_manager.get_secret('ssrs_credentials', 'username')

        # Combining the domain and username with a single slash
        self.username = f"{domain}\\{username}"

        self.password = self.secret_manager.get_secret('ssrs_credentials', 'password')

        with open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r') as config_file:
            self.config = yaml.safe_load(config_file)

        self.BASE_URL = self.config['ssrs']['ReportServer_url']

    def _construct_url(self, data_source_name):
        data_source = self.config['ssrs']['data_sources'][data_source_name]
        report_path = quote(data_source['report_path'])
        parameters = "&".join([f"{quote(key)}={quote(str(value))}" for key, value in data_source['parameters'].items()])
        return f"{self.BASE_URL}{report_path}?{parameters}"

    def connect(self):
        # For SSRS, there is no traditional "connect" step since it's more about HTTP requests
        pass

    def extract(self, data_source_name=None, output_path=None, filename=None, **overridden_parameters):
        # Use default values if not provided
        output_path = output_path or os.getcwd()
        filename = filename or "outputfile.csv"

        # If no data source is specified or the specified data source is invalid, raise an error
        if not data_source_name:
            raise ValueError("A data_source_name must be specified.")
    
        if data_source_name not in self.config['ssrs']['data_sources']:
            raise ValueError(f"The specified data_source_name '{data_source_name}' is not valid. Choose from {list(self.config['ssrs']['data_sources'].keys())}.")

        # Override the default parameters with the manually specified ones
        data_source_config = self.config['ssrs']['data_sources'][data_source_name]
        data_source_config['parameters'].update(overridden_parameters)

        # Construct the full URL and path for the output file
        url = self._construct_url(data_source_name)
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
