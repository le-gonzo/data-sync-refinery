from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from etl.base.base_loader import BaseLoader
from config_management.factory import get_secret_manager

class SQLAlchemyLoader(BaseLoader):
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)

    def connect(self):
        pass  # No explicit connection setup is needed with SQLAlchemy

    def validate(self, data):
        pass  # Implement data validation logic if needed

    def load(self, data):
        # Assuming data is a list of SQLAlchemy model objects
        session = self.Session()
        try:
            session.bulk_save_objects(data)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def close(self):
        pass  # No explicit closing needed with SQLAlchemy
