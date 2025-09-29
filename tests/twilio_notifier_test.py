import os
from unittest import TestCase

from dotenv import load_dotenv
from notihub.notifiers.twilio.notifier import TwilioNotifier


class TestTwilioNotifier(TestCase):
    """TestTwilioNotifier"""

    def setUp(self):
        """Set up"""
        load_dotenv(".env")
        self.account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        self.auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.twilio_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")
        self.to_phone_number = "+19702927873"
        self.message_body = "Test SMS message"
        self.twilio_notifier = TwilioNotifier(
            account_sid=self.account_sid,
            auth_token=self.auth_token,
            twilio_phone_number=self.twilio_phone_number,
        )

    def test_send_sms_notification_success(self):
        """Test sending SMS notification successfully."""
        response_sid = self.twilio_notifier.send_sms_notification(
            phone_number=self.to_phone_number,
            message=self.message_body,
        )
        self.assertIsNotNone(response_sid)

    def test_send_sms_notification_no_twilio_phone_number(self):
        """Test sending SMS notification without a Twilio phone number."""
        self.twilio_notifier.twilio_phone_number = None
        with self.assertRaisesRegex(ValueError, "Twilio phone number must be provided for sending SMS."):
            self.twilio_notifier.send_sms_notification(
                phone_number=self.to_phone_number,
                message=self.message_body,
            )

    def test_send_email_notification_not_implemented(self):
        """Test send_email_notification raises NotImplementedError."""
        with self.assertRaises(NotImplementedError):
            self.twilio_notifier.send_email_notification(
                subject="Test", email_data={}, recipients=[], sender="", template=""
            )

    def test_send_push_notification_not_implemented(self):
        """Test send_push_notification raises NotImplementedError."""
        with self.assertRaises(NotImplementedError):
            self.twilio_notifier.send_push_notification(device="test_device", message="test_message")

    def test_initialization_without_credentials_raises_error(self):
        """Test initialization without credentials raises ValueError."""
        with self.assertRaisesRegex(ValueError, "Twilio Account SID and Auth Token must be provided."):
            TwilioNotifier(account_sid=None, auth_token=None)
