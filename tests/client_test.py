import os
from unittest import TestCase

from dotenv import load_dotenv

from notihub.client import NotifierClient
from notihub.notifiers.aws.notifier import AWSNotifier


class TestNotifierClient(TestCase):
    """TestNotifierClient"""

    def setUp(self):
        """Set up"""
        load_dotenv(".env")

    def test_get_aws_notifier_returns_aws_notifier(self):
        """Test get_aws_notifier"""
        aws_notifier = NotifierClient.get_aws_notifier(
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
            region_name="us-east-2",
        )
        self.assertIsInstance(aws_notifier, AWSNotifier)

    def test_get_aws_client_without_credentials_returns_aws_notifier(self):
        """Test get_aws_notifier"""
        aws_notifier = NotifierClient.get_aws_notifier()
        self.assertIsInstance(aws_notifier, AWSNotifier)
