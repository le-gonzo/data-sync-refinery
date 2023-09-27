import boto3
from .abstract_manager import AbstractSecretManager

class AWSSecretManager(AbstractSecretManager):
    """AWS-specific implementation of the secret manager using AWS Secrets Manager service."""
    
    def __init__(self, region_name="us-west-2"):
        self.client = boto3.client('secretsmanager', region_name=region_name)

    def get_secret(self, key: str) -> str:
        """Retrieve a secret value from AWS Secrets Manager associated with a given key."""
        try:
            response = self.client.get_secret_value(SecretId=key)
            if 'SecretString' in response:
                return response['SecretString']
            # Handle other cases like binary secrets if necessary
        except Exception as e:
            # Handle exceptions, possibly re-raise or log them
            raise e

    def set_secret(self, key: str, value: str) -> None:
        """Set a secret value in AWS Secrets Manager for a given key."""
        try:
            self.client.put_secret_value(SecretId=key, SecretString=value)
        except Exception as e:
            # Handle exceptions, possibly re-raise or log them
            raise e
