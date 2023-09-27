"""Module defining an abstract base class for secret management."""

from abc import ABC, abstractmethod


class AbstractSecretManager(ABC):
    """Abstract base class for secret managers.
    
    This class provides a contract that all secret manager implementations 
    should follow, ensuring consistent interaction regardless of the 
    underlying secret management system.
    """

    @abstractmethod
    def get_secret(self, key: str) -> str:
        """Retrieve a secret value associated with a given key.
        
        Args:
            key (str): The key corresponding to the secret.
        
        Returns:
            str: The secret value.
        
        Raises:
            NotImplementedError: If the method is not implemented 
                by a concrete subclass.
        """
        pass

    @abstractmethod
    def set_secret(self, key: str, value: str) -> None:
        """Set a secret value for a given key.
        
        Args:
            key (str): The key for which the secret should be set.
            value (str): The secret value to be set.
        
        Raises:
            NotImplementedError: If the method is not implemented 
                by a concrete subclass.
        """
        pass
