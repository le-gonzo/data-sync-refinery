from abc import ABC, abstractmethod

class BaseLoader(ABC):

    @abstractmethod
    def connect(self):
        """Establish a connection to the destination."""
        pass

    @abstractmethod
    def validate(self, data):
        """Validate the data before loading. This can be a no-op for some loaders."""
        pass

    @abstractmethod
    def load(self, data):
        """Load the validated data to the destination."""
        pass

    @abstractmethod
    def close(self):
        """Close any connections or finalize loading."""
        pass
