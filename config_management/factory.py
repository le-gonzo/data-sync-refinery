import configparser
from abc import ABC, abstractmethod
from typing import Type, Dict

# --- Configuration Loading ---

def load_configuration() -> str:
    """Load and return the SECRET_MANAGER value from the configuration file."""
    config = configparser.ConfigParser()
    config.read('../config.ini')

    try:
        manager = config['General']['SECRET_MANAGER']
    except KeyError:
        raise ValueError("SECRET_MANAGER is not defined in the config.ini file.")
    
    if manager not in managers.keys():
        supported_managers = ', '.join(managers.keys())
        raise ValueError(f"Unsupported SECRET_MANAGER value: {manager}. Supported values are: {supported_managers}")
    
    return manager

SECRET_MANAGER = load_configuration()

# --- Abstract Base Class ---

class AbstractSecretManager(ABC):
    """Abstract base class that defines methods for managing secrets."""

    @abstractmethod
    def get_secret(self, key: str) -> str:
        """Retrieve secret for a given key."""
        pass

    @abstractmethod
    def set_secret(self, key: str, value: str):
        """Set a secret for a given key."""
        pass

# --- Concrete Implementations ---

class AWSSecretManager(AbstractSecretManager):
    """AWS-specific implementation of secret manager."""

    def get_secret(self, key: str) -> str:
        # TODO: Implement AWS-specific code to fetch a secret
        pass

    def set_secret(self, key: str, value: str):
        # TODO: Implement AWS-specific code to set a secret
        pass

class AzureKeyVaultManager(AbstractSecretManager):
    """Azure-specific implementation of secret manager."""

    def get_secret(self, key: str) -> str:
        # TODO: Implement Azure-specific code to fetch a secret
        pass

    def set_secret(self, key: str, value: str):
        # TODO: Implement Azure-specific code to set a secret
        pass

# --- Secret Managers Dictionary ---

managers: Dict[str, Type['AbstractSecretManager']] = {
    'AWS': AWSSecretManager,
    'AZURE': AzureKeyVaultManager
    # Add other secret managers as needed
}

# --- Factory Function ---

def get_secret_manager() -> AbstractSecretManager:
    """Return an instance of the secret manager based on the configuration.

    Returns:
        AbstractSecretManager: An instance of a concrete secret manager implementation.

    Raises:
        ValueError: If the specified secret manager in the configuration is not supported.
    """
    try:
        return managers[SECRET_MANAGER]()
    except KeyError:
        supported_managers = ', '.join(managers.keys())
        raise ValueError(f"Unsupported secret manager: {SECRET_MANAGER}. Supported managers are: {supported_managers}")
