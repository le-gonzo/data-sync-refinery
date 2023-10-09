# extractors/ssrs_extractor.py
import os
import requests
import yaml
import logging
import configparser
from urllib.parse import quote
from requests_ntlm import HttpNtlmAuth
from typing import Tuple, Optional, Dict

from etl.base.base_extractor import BaseExtractor
from config_management.factory import get_secret_manager

# TODO: Remove magic strings and create constants

class ConfigLoader:
    """Load and parse configuration settings."""

    @staticmethod
    def load_config(file_name='config.ini'):
        config = configparser.ConfigParser()
        config.read(file_name)
        return config
    
    @staticmethod
    def load_yml_config(file_name):
        with open(file_name, 'r') as config_file:
            return yaml.safe_load(config_file)


class SSRSExtractor(BaseExtractor):
    """
    Extractor for SSRS (SQL Server Reporting Services).

    This extractor interfaces with SSRS to extract data based on provided configurations.
    It leverages NTLM authentication and can be utilized in debugging mode for additional interactivity.

    Attributes:
        secret_manager: A manager for handling secrets required for extraction.
    """

    secret_manager = get_secret_manager()

    def __init__(self):
        """
        Initializes the SSRSExtractor, setting up configurations, credentials, and logging level.
        """
        self.config = ConfigLoader.load_yml_config(os.path.join(os.path.dirname(__file__), 'config.yml'))
        self.username, self.password = self.__load_credentials()
        self.BASE_URL = self.config['ssrs']['ReportServer_url']
        
        logging_level = self.config['general']['logging_level'].upper()
        numeric_level = getattr(logging, logging_level, logging.INFO)
        logging.basicConfig(level=numeric_level)



    def __load_credentials(self) -> Tuple[str, str]:
        """
        Retrieves SSRS credentials from the secret manager.

        Returns:
            tuple: A tuple containing full_username and password for SSRS authentication.
        """
        domain = self.secret_manager.get_secret('ssrs_credentials', 'domain')
        username = self.secret_manager.get_secret('ssrs_credentials', 'username')
        full_username = f"{domain}\\{username}"
        password = self.secret_manager.get_secret('ssrs_credentials', 'password')
        return full_username, password

    def __construct_url(self, data_source_name: str) -> str:
        """
        Constructs the SSRS URL for data extraction based on the data source name.

        Args:
            data_source_name (str): The name of the data source for which the URL is to be constructed.

        Returns:
            str: A fully-constructed SSRS URL for the specified data source.
        """
        data_source = self.config['ssrs']['data_sources'][data_source_name]
        report_path = quote(data_source['report_path'], safe = '') #urllib.parse ignores '/' by default but we need to encode it for this portion
        parameters = "&".join([f"{quote(key, safe = '')}={quote(str(value), safe = '')}" for key, value in data_source['parameters'].items()])
        return f"{self.BASE_URL}?{report_path}&{parameters}"
    
    def __prompt_for_confirmation(self, full_path) -> None:
        """
        Prompts the user for a confirmation based on the provided path. Intended for debugging purposes.

        Args:
            full_path (str): The full path or URL that has been generated.

        Raises:
            Exception: If the user does not confirm the operation.
        """
        print(f"Generated full path: {full_path}")
        user_input = input("Do you want to proceed? (Y/N): ").strip().lower()
        
        if user_input != 'y':
            raise Exception("Operation aborted by user.")

    def connect(self) -> None:
        """
        Placeholder for traditional DB connection. 
        SSRS does not require a traditional connection as it's based on HTTP requests.
        """
        pass

    def extract(self, 
                data_source_name: Optional[str] = None, 
                output_path: Optional[str] = None, 
                filename: Optional[str] = None, 
                **overridden_parameters) -> str:
        """
        Extracts data from SSRS based on the provided data source name.

        This method constructs the SSRS URL, makes an HTTP request, and if successful, saves the result to a file.

        Args:
            data_source_name (str, optional): The name of the data source to extract from. Required.
            output_path (str, optional): The path to save the extracted file. Defaults to the current working directory.
            filename (str, optional): The name of the file to save the extracted data. Defaults to "outputfile.csv".
            **overridden_parameters: Any parameters that should override the default parameters for the data source.

        Returns:
            str: The path to the saved extracted file.

        Raises:
            ValueError: If data_source_name is not provided or is not valid.
            Exception: If the request to SSRS fails.
        """
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
        url = self.__construct_url(data_source_name)
        full_path = os.path.join(output_path, filename)


        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            self.__prompt_for_confirmation(url)

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
        
    def validate_connection(self):
        """Validates if the connection to the source is successful."""
        # This can be implemented to make a test request to SSRS to ensure the connection is valid

    def handle_error(self, error):
        """Handles errors during extraction."""
        logging.error(f"Error during extraction: {str(error)}")
        # Further error handling can be added as needed

    def retry(self, n):
        """Sets the number of retries in case of failed extraction attempts."""
        # This can be implemented to retry the extraction in case of certain failures

    def log(self, message, level):
        """Logs various events or messages."""
        numeric_level = getattr(logging, level.upper(), None)
        if numeric_level is not None:
            logging.log(numeric_level, message)
        else:
            logging.info(message)

    def get_metadata(self):
        """Retrieves metadata about the extracted data."""
        # Placeholder for fetching metadata, can be implemented based on the SSRS capabilities
        pass


    def transform_at_source(self, transformation):
        """Allows for light transformations at the source itself."""
        # This can be implemented if SSRS allows for certain transformations during the extraction process

    def set_query(self, query):
        """Set a specific query for data extraction (mainly for databases)."""
        # This can be implemented if SSRS supports query-based data extraction

    def close(self) -> None:
        """
        Placeholder for traditional DB close operation.
        SSRS does not require a traditional close as it's based on HTTP requests.
        """
        pass


if __name__ == "__main__":
    """
    This section provides a hands-on guide on how to use and debug the SSRSExtractor.
    """

    # 1. Initialize logging
    ConfigLoader.initialize_logging()
    
    # 2. Create an instance of SSRSExtractor
    extractor = SSRSExtractor()
    
    # EXAMPLE USAGE:
    # ---------------
    # The following steps guide you on how to utilize the SSRSExtractor to extract data.

    try:
        # Example data source name; you'd replace this with a valid source from your config.
        data_source_name = "your_data_source_name_here"

        # Extract data and print the resulting path
        result_path = extractor.extract(data_source_name=data_source_name)
        print(f"Data successfully extracted to: {result_path}")
    except Exception as e:
        logging.error(f"An error occurred while extracting: {e}")

    # DEBUGGING:
    # ----------
    # If you encounter issues, here are steps to help you debug:

    # a. Ensure your logging level is set to DEBUG in config.ini for detailed logs.
    # b. Check your data source configurations in config.yml.
    # c. Ensure your credentials (e.g., for SSRS) are correctly set in the secret manager.
    
    # ADDITIONAL UTILITIES:
    # ---------------------
    # The SSRSExtractor also provides a `connect` and `close` method, even though they are 
    # not traditionally used for SSRS (which is based on HTTP requests). You can use them 
    # if you extend the class for other systems that require connection handling.

    # Remember, the `extract` method allows for optional parameters like output_path and 
    # filename. You can use them to specify custom save locations or filenames.

    # e.g., 
    # result = extractor.extract(data_source_name=data_source_name, output_path="/path/to/save", filename="custom_name.csv")