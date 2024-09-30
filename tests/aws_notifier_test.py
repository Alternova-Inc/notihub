import os
from unittest import TestCase

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from notifiers.aws.notifier import AWSNotifier


class TestAWSNotifier(TestCase):
    """TestAWSNotifier"""

    def setUp(self):
        """Set up"""
        load_dotenv("../.env")
        self.aws_notifier = AWSNotifier(
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
            region_name="us-east-2",
        )
        self.topic_name = "test-topic-notipy"
        self.sns_client = boto3.client(
            "sns",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
            region_name="us-east-2",
        )
        self.ses_client = boto3.client(
            "ses",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
            region_name="us-east-2",
        )

    def tearDown(self) -> None:
        if getattr(self, "topic_arn", None):
            self.aws_notifier.delete_topic(self.topic_arn)
        if getattr(self, "template_name", None):
            self.aws_notifier.delete_email_template(self.template_name)

    def test_class_initialization_sets_clients(self):
        """Test class initialization"""
        self.assertIsNotNone(self.aws_notifier.sns_client)
        self.assertIsNotNone(self.aws_notifier.ses_client)

    def test_create_client_returns_boto3_client(self):
        """Test create_client"""
        self.assertIsNotNone(self.aws_notifier.create_client("sns"))

    def test_create_topic_creates_topic(self):
        """Test create_topic"""
        topic = self.aws_notifier.create_topic(self.topic_name)
        self.topic_arn = topic["TopicArn"]
        self.assertEqual(topic["TopicArn"], self.topic_arn)

    def test_get_topic_gets_topic(self):
        """Test get_topic"""
        topic = self.aws_notifier.create_topic(self.topic_name)
        self.topic_arn = topic["TopicArn"]
        topic = self.aws_notifier.get_topic(self.topic_arn)
        self.assertEqual(topic["Attributes"]["TopicArn"], self.topic_arn)

    def test_delete_topic_deletes_topic(self):
        """Test delete_topic"""
        topic = self.aws_notifier.create_topic(self.topic_name)
        self.topic_arn = topic["TopicArn"]
        self.aws_notifier.delete_topic(self.topic_arn)
        with self.assertRaises(ClientError) as context:
            self.aws_notifier.get_topic(self.topic_arn)
            self.assertEqual(
                context.exception.response["Error"]["Code"],
                "ResourceNotFoundException",
            )

    def test_subscribe_to_topic_subscribes_to_topic(self):
        """Test subscribe_to_topic"""
        topic = self.aws_notifier.create_topic(self.topic_name)
        self.topic_arn = topic["TopicArn"]
        subscription = self.aws_notifier.subscribe_to_topic(
            topic_arn=self.topic_arn,
            protocol="email",
            endpoint="developer.testing72@gmail.com",
        )
        self.assertEqual(subscription["SubscriptionArn"], "pending confirmation")

    def test_send_topic_notification_sends_topic_notification(self):
        """Test send_topic_notification"""
        topic = self.aws_notifier.create_topic(self.topic_name)
        self.topic_arn = topic["TopicArn"]
        response = self.aws_notifier.send_topic_notification(
            topic_arn=self.topic_arn, message="Test message", subject="Test subject"
        )
        self.assertIsNotNone(response["MessageId"])

    def test_send_sms_notification_sends_sms_notification(self):
        """Test send_sms_notification"""
        response = self.aws_notifier.send_sms_notification(
            phone_number="123456789", message="Test message"
        )
        print(response)
        self.assertIsNotNone(response["MessageId"])

    def test_send_email_notification_sends_email_notification(self):
        """Test send_email_notification"""
        response = self.aws_notifier.send_email_notification(
            email_data={"name": "John Doe"},
            recipients=["developer.testing72@gmail.com"],
            sender="test.service@alternovastudio.com",
            template="test",
        )
        self.assertIsNotNone(response["MessageId"])

    def test_send_email_notification_with_subject_changes_template_subject(self):
        """Test send_email_notification"""
        self.aws_notifier.create_email_template(
            template_name="test-notipy",
            subject="Test subject",
            text_body="Test text body",
            html_body="Test html body",
        )
        self.aws_notifier.send_email_notification(
            email_data={"name": "John Doe"},
            recipients=["developer.testing72@gmail.com"],
            sender="test.service@alternovastudio.com",
            template="test-notipy",
            subject="New subject",
        )
        updated_template = self.aws_notifier.get_email_template(
            template_name="test-notipy"
        )
        self.aws_notifier.delete_email_template(template_name="test-notipy")
        self.assertEqual(updated_template["Template"]["SubjectPart"], "New subject")

    def test_send_push_notification_sends_push_notification(self):
        """Test send_push_notification"""
        response = self.aws_notifier.send_push_notification(
            device=os.environ.get("DEVICE_ARN"),
            message="Test message",
        )
        self.assertIsNotNone(response["MessageId"])

    def test_create_email_template_creates_email_template(self):
        """Test create_email_template"""
        response = self.aws_notifier.create_email_template(
            template_name="test-template",
            subject="Test subject",
            text_body="Test text body",
            html_body="Test html body",
        )
        self.template_name = "test-template"
        self.assertIsNotNone(response["ResponseMetadata"]["RequestId"])

    def test_update_email_template_updates_email_template(self):
        """Test update_email_template"""
        self.aws_notifier.create_email_template(
            template_name="test-template",
            subject="Test subject",
            text_body="Test text body",
            html_body="Test html body",
        )
        self.template_name = "test-template"
        response = self.aws_notifier.update_email_template(
            template_name="test-template",
            subject="Updated subject",
            text_body="Updated text body",
            html_body="Updated html body",
        )
        self.assertIsNotNone(response["ResponseMetadata"]["RequestId"])

    def test_list_email_templates_lists_email_templates(self):
        """Test list_email_templates"""
        response = self.aws_notifier.list_email_templates()
        self.assertIsNotNone(response["ResponseMetadata"]["RequestId"])

    def test_get_email_template_gets_email_template(self):
        """Test get_email_template"""
        self.aws_notifier.create_email_template(
            template_name="test-template",
            subject="Test subject",
            text_body="Test text body",
            html_body="Test html body",
        )
        self.template_name = "test-template"
        response = self.aws_notifier.get_email_template(template_name=self.template_name)
        self.assertIsNotNone(response["ResponseMetadata"]["RequestId"])

    def test_delete_email_template_deletes_email_template(self):
        """Test delete_email_template"""
        self.aws_notifier.create_email_template(
            template_name="test-template",
            subject="Test subject",
            text_body="Test text body",
            html_body="Test html body",
        )
        self.template_name = "test-template"
        response = self.aws_notifier.delete_email_template(
            template_name=self.template_name
        )
        self.assertIsNotNone(response["ResponseMetadata"]["RequestId"])
