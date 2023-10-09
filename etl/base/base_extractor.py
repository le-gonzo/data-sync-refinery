from abc import ABC, abstractmethod

class BaseExtractor(ABC):

    @abstractmethod
    def connect(self):
        """Establish a connection to the data source."""
        pass

    @abstractmethod
    def validate_connection(self):
        """Validates if the connection to the source is successful."""
        pass

    @abstractmethod
    def extract(self):
        """Extract data from the source."""
        pass

    @abstractmethod
    def preview(self, n=5):
        """Preview a subset of the data (default: first 5 records)."""
        pass

    @abstractmethod
    def set_extraction_point(self, point):
        """Sets a starting point for incremental extraction."""
        pass

    @abstractmethod
    def get_last_extraction_point(self):
        """Retrieves the last extraction point."""
        pass

    @abstractmethod
    def set_query(self, query):
        """Set a specific query for data extraction (mainly for databases)."""
        pass

    @abstractmethod
    def transform_at_source(self, transformation):
        """Allows for light transformations at the source itself."""
        pass

    @abstractmethod
    def get_metadata(self):
        """Retrieves metadata about the extracted data."""
        pass

    @abstractmethod
    def handle_error(self, error):
        """Handles errors during extraction."""
        pass

    @abstractmethod
    def retry(self, n):
        """Sets the number of retries in case of failed extraction attempts."""
        pass

    @abstractmethod
    def log(self, message, level):
        """Logs various events or messages."""
        pass

    @abstractmethod
    def close(self):
        """Close any connections."""
        pass