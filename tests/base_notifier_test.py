from unittest import TestCase

from base_notifier import BaseNotifier


class TestBaseNotifier(BaseNotifier):
    """TestBaseNotifier"""

    def send_sms_notification(self, phone_number: str, message: str, **kwargs) -> str:
        """Sends a SMS notification to the given phone number"""
        return "SMS notification sent"

    def send_email_notification(
        self,
        *,
        subject: str,
        email_data: dict,
        recipients: list,
        sender: str,
        template: str,
        cc_emails: list = None,
        bcc_emails: list = None,
        **kwargs,
    ) -> str:
        """Sends an email notification to the given email"""
        return "Email notification sent"

    def send_push_notification(self, message: str, **kwargs) -> str:
        """Sends a push notification to the given message"""
        return "Push notification sent"


class TestBaseNotifierTests(TestCase):
    """TestBaseNotifierTests"""

    def test_send_sms_notification(self):
        """Test send_sms_notification"""
        notifier = TestBaseNotifier()
        result = notifier.send_sms_notification(
            phone_number="123456789", message="Test message"
        )
        self.assertEqual(result, "SMS notification sent")

    def test_send_email_notification(self):
        """Test send_email_notification"""
        notifier = TestBaseNotifier()
        result = notifier.send_email_notification(
            subject="Test subject",
            email_data={"name": "John Doe"},
            recipients=["developer.testing72@gmail.com"],
            sender="test.service@alternovastudio.com",
            template="test",
        )
        self.assertEqual(result, "Email notification sent")

    def test_send_push_notification(self):
        """Test send_push_notification"""
        notifier = TestBaseNotifier()
        result = notifier.send_push_notification(message="Test message")
        self.assertEqual(result, "Push notification sent")
