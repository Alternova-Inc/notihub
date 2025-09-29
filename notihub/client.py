"""

Base client for notifiers

This module contains the base client for notifiers it is used to access the notifiers
via interface

"""

from typing import Type, Optional

from notihub.notifiers.aws.notifier import AWSNotifier


class NotifierClient:
    """
    Notifier client

    Used as interface to access notifiers
    """

    @staticmethod
    def get_aws_notifier(
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        region_name: Optional[str] = None
    ) -> Type[AWSNotifier]:
        """
        Returns an AWS notifier client
        
        If no credentials are provided, the default ones will be used
        using boto3 default config handling
        """
        return AWSNotifier(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )
