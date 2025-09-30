"""

Twilio Notifier

This module contains the Twilio notifier class which is used to send notifications via Twilio
"""

from dataclasses import dataclass
from typing import List, Optional

from twilio.rest import Client

from notihub.base_notifier import BaseNotifier


@dataclass
class TwilioNotifier(BaseNotifier):
    """
    TwilioNotifier

    Class used to send notifications via Twilio
    """

    account_sid: Optional[str] = None
    auth_token: Optional[str] = None
    twilio_phone_number: Optional[str] = None

    def __post_init__(self):
        if not self.account_sid or not self.auth_token:
            raise ValueError(
                "Twilio Account SID and Auth Token must be provided."
            )

        self.client = Client(self.account_sid, self.auth_token)

    def send_sms_notification(self, phone_number: str, message: str, **kwargs) -> str:
        """Sends a SMS notification to the given phone number using Twilio."""
        if not self.twilio_phone_number:
            raise ValueError("Twilio phone number must be provided for sending SMS.")

        message = self.client.messages.create(
            to=phone_number,
            from_=self.twilio_phone_number,
            body=message,
            **kwargs,
        )
        return message.sid

    def send_email_notification(
        self,
        *,
        subject: str,
        email_data: dict,
        recipients: List[str],
        sender: str,
        template: str,
        cc_emails: List[str] = None,
        bcc_emails: List[str] = None,
        **kwargs,
    ) -> str:
        """Sends an email notification to the given email (not supported by Twilio directly for this library)."""
        raise NotImplementedError("Twilio does not directly support email notifications in this library.")

    def send_push_notification(self, device: str, message: str, **kwargs) -> str:
        """Sends a push notification to the given message (not supported by Twilio directly for this library)."""
        raise NotImplementedError("Twilio does not directly support push notifications in this library.")
