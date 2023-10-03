import configparser
from sqlalchemy import create_engine, exc
import os
import psycopg2


class DatabaseConfigError(Exception):
    """Exception raised for errors in the database configuration."""


class ConfigLoader:
    @staticmethod
    def load(config_path, db_type):
        """
        Load the configuration for the specified database type from the provided path.
        """
        config = configparser.ConfigParser(interpolation=None)
        config.read(config_path)

        if db_type not in config:
            raise DatabaseConfigError(f"No configuration section found for database type: {db_type}")

        # retrieve the entire section as a dictionary
        section = dict(config.items(db_type))

        # Handle special characters in the password
        #section['db_password'] = section['db_password'] #Redundent


        # print out the section for debugging
        # print("DEBUG - Configuration Dictionary:")
        # for key, value in section.items():
        #    print(f"{key}: {value}")


        return section


class ConnectionManager:
    DB_URL_TEMPLATES = {
        "mysql": "mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
        "postgres": "postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    }

    def __init__(self, db_type, config_path):
        """
        Initialize the ConnectionManager with a specific database type and configuration path.
        """
        self.db_type = db_type.lower()
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"The configuration file '{config_path}' was not found.")

        self._connection = None
        self._engine = None
        self._config = ConfigLoader.load(config_path, self.db_type)

    @property
    def engine(self):
        """Lazy-load and return the SQLAlchemy engine."""
        if self._engine is None:
            self._engine = create_engine(self._create_engine_url())
        return self._engine

    def _create_engine_url(self):
        """Construct and return the SQLAlchemy engine URL based on the configuration."""

        db_user = self._config['db_user']
        # Double the '%' character for SQLAlchemy, then URI encode the password
        db_password = self._config['db_password']
        db_host = self._config['db_host']
        db_port = self._config['db_port']
        db_name = self._config['db_name']

        # Using an f-string to format the connection URL
        if self.db_type == "mysql":
            connection_url = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        elif self.db_type == "postgres":
            connection_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        else:
            raise ValueError(f"Unsupported db_type: {self.db_type}")
        
        # Print the connection_url for debugging
        # print("DEBUG Connection URL:", connection_url)

        return connection_url

    def get_connection(self):
        """Establish and return a connection to the database."""
        if self._connection is None:
            try:
                self._connection = self.engine.connect()
            except exc.OperationalError as oe:
                raise ConnectionError("Failed to connect to the database. Please check your server and credentials.") from oe
        return self._connection

    def close(self):
        """Close the current database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None

    def __enter__(self):
        """Provide a context manager interface for the connection."""
        return self.get_connection()

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        """Close the connection when exiting the context."""
        self.close()


if __name__ == "__main__":
    db_type = "postgres"
    config_path = "C:/Users/lgonzal1/db_credentials.ini"
    
    try:
        with ConnectionManager(db_type, config_path) as conn:
            result = conn.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
            for row in result:
                print(row)
    except Exception as e:
        print(f"Error occurred: {e}")
