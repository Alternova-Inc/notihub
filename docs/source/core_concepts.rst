Core Concepts
=============

BaseNotifier Abstract Class
---------------------------

The ``BaseNotifier`` abstract class serves as the foundation for all notification providers in NotiHub. It defines the standard interface that all notifiers must implement, ensuring consistency across different services.

All notifiers in NotiHub inherit from the ``BaseNotifier`` abstract class, which defines three core methods:

*   ``send_sms_notification()``: For sending SMS messages
*   ``send_email_notification()``: For sending email notifications
*   ``send_push_notification()``: For sending push notifications

This abstraction allows developers to write code that works with any supported notification provider without modification.

.. code-block:: python

    from abc import ABC, abstractmethod
    from dataclasses import dataclass
    from typing import List

    @dataclass
    class BaseNotifier(ABC):
        """Base class for all notifiers used to register them"""

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