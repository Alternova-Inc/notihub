"""

AWS Notifier

This module contains the AWS notifier class which is used to send notifications via AWS
SNS, SES or Pinpoint
"""

from dataclasses import dataclass

from notihub.base_notifier import BaseNotifier
from notihub.notifiers.aws.clients.pinpoint_client import PinpointClient
from notihub.notifiers.aws.clients.ses_client import SESClient
from notihub.notifiers.aws.clients.sns_client import SNSClient


@dataclass
class AWSNotifier(SNSClient, SESClient, PinpointClient, BaseNotifier):
    """
    AWSNotifier

    Centralized class to send notifications via AWS SNS, SES or Pinpoint using
    class inheritance to initialize the clients.
    """

    aws_access_key_id: str = None
    aws_secret_access_key: str = None
    region_name: str = None

    def __post_init__(self):
        """
        Initializes the parent client classes after AWSNotifier's own fields are set.
        This ensures that self.sns_client, self.ses_client, and self.pinpoint_client
        are created by their respective parent classes.
        """
        SNSClient.__post_init__(self)
        SESClient.__post_init__(self)
        PinpointClient.__post_init__(self)
