import yaml
from config_management.abstract_manager import AbstractSecretManager

class YAMLSecretManager(AbstractSecretManager):
    """
    A general implementation of a configuration manager using a YAML file.

    Note: This is suitable for development/testing purposes only and 
    should not be used in production environments or with real secrets.
    """

    def __init__(self, filepath: str) -> None:
        """Initialize the YAML Secret Manager."""
        self.filepath = filepath
        with open(self.filepath, 'r') as file:
            self.config = yaml.safe_load(file)

    def get_secret(self, section: str, key: str) -> str:
        """
        Retrieve a value associated with a given section and key.

        Args:
            section (str): The section in the YAML file.
            key (str): The key corresponding to the desired value.
        
        Returns:
            str: The corresponding value.

        Raises:
            ValueError: If the section or key is not found in the file.
        """
        try:
            return self.config[section][key]
        except KeyError:
            raise ValueError(f"Section '{section}' or Key '{key}' not found in {self.filepath}.")

    def set_secret(self, section: str, key: str, value: str) -> None:
        """
        Set a value for a given section and key in the YAML file.

        Args:
            section (str): The section in the YAML file.
            key (str): The key for which the value should be set.
            value (str): The value to be set.
        """
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        with open(self.filepath, 'w') as file:
            yaml.safe_dump(self.config, file)
