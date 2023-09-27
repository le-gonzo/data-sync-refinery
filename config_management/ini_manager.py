import configparser
from config_management.abstract_manager import AbstractSecretManager

class INISecretManager(AbstractSecretManager):
    """
    A basic implementation of a secret manager using an INI file.

    Note: This is suitable for development/testing purposes only and 
    should not be used in production environments or with real secrets.
    """

    def __init__(self) -> None:
        """Initialize the INI Secret Manager."""
        self.config = configparser.ConfigParser()
        self.config.read('../secrets.ini')

    def get_secret(self, key: str) -> str:
        """
        Retrieve a secret value associated with a given key.

        Args:
            key (str): The key corresponding to the secret.
        
        Returns:
            str: The secret value.

        Raises:
            ValueError: If the key is not found in the secrets.ini file.
        """
        try:
            return self.config['Secrets'][key]
        except KeyError:
            raise ValueError(f"Key {key} not found in secrets.ini file.")

    def set_secret(self, key: str, value: str) -> None:
        """
        Set a secret value for a given key in the secrets.ini file.

        Args:
            key (str): The key for which the secret should be set.
            value (str): The secret value to be set.
        """
        if 'Secrets' not in self.config:
            self.config['Secrets'] = {}
        self.config['Secrets'][key] = value
        with open('../secrets.ini', 'w') as configfile:
            self.config.write(configfile)
