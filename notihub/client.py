"""

Base client for notifiers

This module contains the base client for notifiers it is used to access the notifiers
via interface

"""

from typing import Type

from notihub.notifiers.aws.notifier import AWSNotifier


class NotifierClient:
    """
    Notifier client

    Used as interface to access notifiers
    """

    @staticmethod
    def get_aws_notifier(
        aws_access_key_id: str, aws_secret_access_key: str, region_name: str
    ) -> Type[AWSNotifier]:
        """Returns an AWS notifier client"""
        return AWSNotifier(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )
