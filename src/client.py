import os
from typing import Type

from dotenv import load_dotenv

from notifiers.aws.notifier import AWSNotifier


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


load_dotenv("../.env")
aws_notifier = NotifierClient.get_aws_notifier(
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
    region_name="us-east-2",
)


print(
    aws_notifier.send_email_notification(
        email_data={"name": "John Doe"},
        recipients=["juan.trujillo@alternova.com"],
        sender="test.service@alternovastudio.com",
        template="test",
    )
)
