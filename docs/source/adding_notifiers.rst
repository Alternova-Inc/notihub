Adding New Notifiers
====================

NotiHub is designed to be easily extensible. Adding a new notification provider involves:

1.  Creating a new provider directory structure
2.  Implementing the ``BaseNotifier`` interface
3.  Adding a factory method to the client
4.  Creating comprehensive tests

Step-by-Step Guide
------------------

1.  **Create Provider Directory Structure**

    .. code-block:: bash

        mkdir -p notihub/notifiers/your_provider/
        touch notihub/notifiers/your_provider/__init__.py
        touch notihub/notifiers/your_provider/notifier.py

2.  **Implement BaseNotifier Interface**

    .. code-block:: python

        from dataclasses import dataclass
        from typing import List
        from notihub.base_notifier import BaseNotifier

        @dataclass
        class YourNotifier(BaseNotifier):
            """Your custom notification provider"""

            # Provider-specific configuration
            api_key: str = None
            api_secret: str = None

            def send_sms_notification(self, phone_number: str, message: str, **kwargs) -> str:
                """Implement SMS sending logic"""
                # Your SMS implementation
                pass

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
                """Implement email sending logic"""
                # Your email implementation
                pass

            def send_push_notification(self, device: str, message: str, **kwargs) -> str:
                """Implement push notification logic"""
                # Your push implementation
                pass

3.  **Add Factory Method to Client**

    .. code-block:: python

        # In notihub/client.py
        from notihub.notifiers.your_provider.notifier import YourNotifier

        class NotifierClient:
            @staticmethod
            def get_your_notifier(api_key: str = None, api_secret: str = None) -> YourNotifier:
                """Returns a YourProvider notifier client"""
                return YourNotifier(api_key=api_key, api_secret=api_secret)

4.  **Create Comprehensive Tests**

    .. code-block:: python

        # tests/your_notifier_test.py
        import unittest
        from notihub.notifiers.your_provider.notifier import YourNotifier

        class TestYourNotifier(unittest.TestCase):
            def setUp(self):
                self.notifier = YourNotifier(api_key="test_key", api_secret="test_secret")

            def test_send_sms_notification(self):
                # Test SMS functionality
                pass

            def test_send_email_notification(self):
                # Test email functionality
                pass

            def test_send_push_notification(self):
                # Test push functionality
                pass

Implementation Guidelines
-------------------------

*   **Required Inheritance**: All notifiers must inherit from ``BaseNotifier`` and implement all abstract methods.
*   **Error Handling**: Implement proper error handling for API failures, network issues, and invalid parameters.
*   **Configuration**: Use dataclasses for configuration to ensure type safety and easy instantiation.
*   **Logging**: Include appropriate logging for debugging and monitoring.
*   **Documentation**: Document all public methods with clear parameter descriptions and return values.