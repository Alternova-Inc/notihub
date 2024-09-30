"""

Base Notifier

This module contains the base notifier class which is the boilerplate for all notifiers
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class BaseNotifier(ABC):
    """
    BaseNotifier

    Base class for all notifiers used to register them
    """

    @abstractmethod
    def send_sms_notification(self, phone_number: str, message: str, **kwargs) -> str:
        """Sends a SMS notification to the given phone number"""

    @abstractmethod
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
        """Sends an email notification to the given email"""

    @abstractmethod
    def send_push_notification(self, device: str, message: str, **kwargs) -> str:
        """Sends a push notification to the given message"""
