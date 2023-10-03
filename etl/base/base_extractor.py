from abc import ABC, abstractmethod

class BaseExtractor(ABC):

    @abstractmethod
    def connect(self):
        """Establish a connection to the data source."""
        pass

    @abstractmethod
    def extract(self):
        """Extract data from the source."""
        pass

    @abstractmethod
    def close(self):
        """Close any connections."""
        pass