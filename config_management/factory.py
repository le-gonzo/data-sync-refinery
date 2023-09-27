import configparser
from abc import ABC, abstractmethod
from importlib import import_module
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
    
    if manager not in manager_module_map.keys():
        supported_managers = ', '.join(manager_module_map.keys())
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

# --- Mapping for Dynamic Imports ---

manager_module_map = {
    'AWS': ('config_management.aws_manager', 'AWSSecretManager'),
    'AZURE': ('config_management.azure_manager', 'AzureKeyVaultManager'),
    'INI': ('config_management.ini_manager', 'INISecretManager')
}

# --- Factory Function ---

def get_secret_manager() -> AbstractSecretManager:
    """Return an instance of the secret manager based on the configuration.

    Returns:
        AbstractSecretManager: An instance of a concrete secret manager implementation.

    Raises:
        ValueError: If the specified secret manager in the configuration is not supported.
    """
    module_name, class_name = manager_module_map[SECRET_MANAGER]
    ManagerClass = getattr(import_module(module_name), class_name)
    return ManagerClass()
