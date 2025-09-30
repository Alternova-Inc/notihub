from dataclasses import dataclass
from abc import ABC

import boto3

@dataclass
class BaseAWSClient(ABC):
    
    aws_access_key_id: str = None
    aws_secret_access_key: str = None
    region_name: str = None

    def initialize_client(self, service_name: str = None):
        """
        Initialize the AWS client
        
        Args:
            service_name (str): The name of the service
        """
        self.validate_credentials()
        kwargs = {}
        if self.aws_access_key_id and self.aws_secret_access_key and self.region_name:
            kwargs["aws_access_key_id"] = self.aws_access_key_id
            kwargs["aws_secret_access_key"] = self.aws_secret_access_key
            kwargs["region_name"] = self.region_name

        return boto3.client(service_name, **kwargs)

    def validate_credentials(self):
        """
        Validate AWS credentials are provided
        """
        required_credentials = list(
            filter(None, [self.aws_access_key_id, self.aws_secret_access_key, self.region_name])
        )
        if required_credentials and not len(required_credentials) == 3:
            raise ValueError(
                "AWS access key ID, secret access key, "
                "and region name must be provided all together."
            )

