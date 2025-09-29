# NotiHub Documentation

## Overview and Philosophy

NotiHub is a Python library designed to manage and use different notification services through a unified, plug-and-play interface. The library's core philosophy centers around providing a consistent abstraction layer over various notification providers, allowing developers to switch between services or use multiple providers simultaneously with minimal code changes.

### Plug-and-Play Design Philosophy

The plug-and-play design philosophy of NotiHub offers several key benefits:

**Consistency**: All notification providers implement the same interface defined by the `BaseNotifier` abstract class, ensuring consistent behavior across different services.

**Flexibility**: Easy to add new notification providers or switch between existing ones without changing application code.

**Maintainability**: Centralized configuration and error handling reduces code duplication and makes maintenance easier.

**Extensibility**: The abstract base class pattern makes it simple to extend functionality for new notification channels or providers.

**Testability**: Consistent interfaces make unit testing straightforward and provider-agnostic.

## Architecture

### BaseNotifier Abstract Base Class

The `BaseNotifier` class serves as the foundation for all notification providers in NotiHub. It defines the standard interface that all notifiers must implement.

```python
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
```

### Directory Structure Organization

NotiHub organizes notification providers in a clear, hierarchical structure:

```
notihub/
├── __init__.py
├── base_notifier.py          # Abstract base class
├── client.py                 # Factory client for notifier instantiation
└── notifiers/
    ├── __init__.py
    ├── aws/                  # AWS notification provider
    │   ├── __init__.py
    │   ├── notifier.py       # Main AWS notifier class
    │   └── clients/          # AWS service-specific clients
    │       ├── __init__.py
    │       ├── base_aws_client.py
    │       ├── sns_client.py
    │       ├── ses_client.py
    │       └── pinpoint_client.py
    └── twilio/               # Twilio notification provider
        ├── __init__.py
        └── notifier.py       # Twilio notifier implementation
```

### Client Factory Pattern

The `NotifierClient` class provides a factory pattern for easy instantiation of notification providers:

```python
from notihub.client import NotifierClient

# AWS Notifier
aws_notifier = NotifierClient.get_aws_notifier(
    aws_access_key_id="your_key",
    aws_secret_access_key="your_secret",
    region_name="us-east-1"
)

# Twilio Notifier
twilio_notifier = NotifierClient.get_twilio_notifier(
    account_sid="your_sid",
    auth_token="your_token",
    twilio_phone_number="your_number"
)
```

## Adding New Notifiers

### Step-by-Step Guide

1. **Create Provider Directory Structure**
   ```bash
   mkdir -p notihub/notifiers/your_provider/
   touch notihub/notifiers/your_provider/__init__.py
   touch notihub/notifiers/your_provider/notifier.py
   ```

2. **Implement BaseNotifier Interface**
   ```python
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
   ```

3. **Add Factory Method to Client**
   ```python
   # In notihub/client.py
   from notihub.notifiers.your_provider.notifier import YourNotifier

   class NotifierClient:
       @staticmethod
       def get_your_notifier(api_key: str = None, api_secret: str = None) -> YourNotifier:
           """Returns a YourProvider notifier client"""
           return YourNotifier(api_key=api_key, api_secret=api_secret)
   ```

4. **Create Comprehensive Tests**
   ```python
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
   ```

### Implementation Guidelines

**Required Inheritance**: All notifiers must inherit from `BaseNotifier` and implement all abstract methods.

**Error Handling**: Implement proper error handling for API failures, network issues, and invalid parameters.

**Configuration**: Use dataclasses for configuration to ensure type safety and easy instantiation.

**Logging**: Include appropriate logging for debugging and monitoring.

**Documentation**: Document all public methods with clear parameter descriptions and return values.

## Usage Examples

### Basic AWS Notifier Usage

```python
from notihub.client import NotifierClient

# Initialize AWS notifier
aws_notifier = NotifierClient.get_aws_notifier(
    aws_access_key_id="your_access_key",
    aws_secret_access_key="your_secret_key",
    region_name="us-east-1"
)

# Send SMS via AWS SNS
aws_notifier.send_sms_notification(
    phone_number="+1234567890",
    message="Hello from NotiHub!"
)

# Send email via AWS SES
aws_notifier.send_email_notification(
    subject="Test Email",
    email_data={"name": "John Doe", "content": "This is a test email"},
    recipients=["john@example.com"],
    sender="noreply@yourapp.com",
    template="welcome_template"
)

# Send push notification via AWS SNS
aws_notifier.send_push_notification(
    device="arn:aws:sns:us-east-1:123456789012:endpoint/APNS_SANDBOX/...",
    message="You have a new notification!",
    title="NotiHub Alert"
)
```

### Twilio Notifier Usage

```python
from notihub.client import NotifierClient

# Initialize Twilio notifier
twilio_notifier = NotifierClient.get_twilio_notifier(
    account_sid="your_account_sid",
    auth_token="your_auth_token",
    twilio_phone_number="+1234567890"
)

# Send SMS via Twilio
twilio_notifier.send_sms_notification(
    phone_number="+0987654321",
    message="Hello from Twilio via NotiHub!"
)
```

### Error Handling and Best Practices

```python
from notihub.client import NotifierClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Initialize notifier
    notifier = NotifierClient.get_aws_notifier()

    # Send notification with error handling
    try:
        result = notifier.send_sms_notification(
            phone_number="+1234567890",
            message="Test message"
        )
        logger.info(f"Notification sent successfully: {result}")

    except Exception as e:
        logger.error(f"Failed to send notification: {str(e)}")
        # Implement retry logic or fallback to another provider

except Exception as e:
    logger.error(f"Failed to initialize notifier: {str(e)}")
```

## API Reference

### BaseNotifier

Abstract base class for all notification providers.

#### Methods

**send_sms_notification(phone_number: str, message: str, **kwargs) -> str**
Sends an SMS notification to the specified phone number.

**Parameters:**
- `phone_number` (str): The recipient's phone number
- `message` (str): The message content to send
- `**kwargs`: Additional provider-specific parameters

**Returns:** str - Provider-specific response identifier

**send_email_notification(*, subject: str, email_data: dict, recipients: List[str], sender: str, template: str, cc_emails: List[str] = None, bcc_emails: List[str] = None, **kwargs) -> str**
Sends an email notification.

**Parameters:**
- `subject` (str): Email subject line
- `email_data` (dict): Template data for email content
- `recipients` (List[str]): List of recipient email addresses
- `sender` (str): Sender email address
- `template` (str): Email template identifier
- `cc_emails` (List[str], optional): CC recipients
- `bcc_emails` (List[str], optional): BCC recipients
- `**kwargs`: Additional provider-specific parameters

**Returns:** str - Provider-specific response identifier

**send_push_notification(device: str, message: str, **kwargs) -> str**
Sends a push notification to a device.

**Parameters:**
- `device` (str): Device identifier (e.g., ARN, token)
- `message` (str): Notification message content
- `**kwargs`: Additional provider-specific parameters

**Returns:** str - Provider-specific response identifier

### NotifierClient

Factory class for creating notification provider instances.

#### Static Methods

**get_aws_notifier(aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] = None, region_name: Optional[str] = None) -> AWSNotifier**
Creates an AWS notification provider instance.

**Parameters:**
- `aws_access_key_id` (str, optional): AWS access key ID
- `aws_secret_access_key` (str, optional): AWS secret access key
- `region_name` (str, optional): AWS region name

**Returns:** AWSNotifier instance

**get_twilio_notifier(account_sid: Optional[str] = None, auth_token: Optional[str] = None, twilio_phone_number: Optional[str] = None) -> TwilioNotifier**
Creates a Twilio notification provider instance.

**Parameters:**
- `account_sid` (str, optional): Twilio account SID
- `auth_token` (str, optional): Twilio auth token
- `twilio_phone_number` (str, optional): Twilio phone number

**Returns:** TwilioNotifier instance

### AWSNotifier

AWS notification provider supporting SNS, SES, and Pinpoint services.

#### Additional Methods

**SNS Operations:**
- `create_topic(topic_name: str) -> Dict[str, Any]`
- `delete_topic(topic_arn: str) -> Dict[str, Any]`
- `subscribe_to_topic(topic_arn: str, protocol: str, endpoint: str) -> Dict[str, Any]`
- `send_topic_notification(topic_arn: str, message: str, subject: str, **kwargs) -> Dict[str, Any]`

**Device Management:**
- `create_device_endpoint(platform_application_arn: str, device_token: str, **kwargs) -> Dict[str, Any]`
- `delete_device_endpoint(endpoint_arn: str, **kwargs) -> Dict[str, Any]`
- `update_device_endpoint(endpoint_arn: str, custom_user_data: str, **kwargs) -> Dict[str, Any]`

## Development and Testing

### Setting Up Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Alternova-Inc/notihub.git
   cd notihub
   ```

2. **Install dependencies:**
   ```bash
   pip install -e .
   pip install -e ".[dev]"
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your provider credentials
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=notihub

# Run specific test file
pytest tests/aws_notifier_test.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code
black notihub/

# Lint code
ruff check notihub/


## Contributing Guidelines

### Development Workflow

1. **Fork the repository** on GitHub
2. **Create a feature branch** from `main`
3. **Make your changes** following the existing code style
4. **Add tests** for new functionality
5. **Update documentation** if needed
6. **Run the test suite** to ensure nothing is broken
7. **Submit a pull request** with a clear description

### Code Style Guidelines

- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all public classes and methods
- Keep line length under 90 characters
- Use dataclasses for configuration objects
- Implement proper error handling and logging

### Adding New Providers

When adding a new notification provider:

1. Follow the step-by-step guide in the "Adding New Notifiers" section
2. Ensure all abstract methods are implemented
3. Add comprehensive unit tests
4. Update this documentation
5. Add configuration examples to README.md

### Testing Requirements

- Minimum 85% test coverage
- Unit tests for all public methods
- Integration tests for external service calls (mocked)
- Error handling tests
- Edge case testing

## Support and Troubleshooting

### Common Issues

**Import Errors**: Ensure all dependencies are installed and the Python path includes the notihub directory.

**Authentication Failures**: Verify that credentials are correctly configured in environment variables or passed to the client factory methods.

**Network Timeouts**: Implement retry logic with exponential backoff for production applications.

### Getting Help

- Check the [GitHub Issues](https://github.com/Alternova-Inc/notihub/issues) for known problems
- Create a new issue with detailed information about your problem
- Include error messages, code snippets, and environment details

## License

NotiHub is released under the MIT License. See LICENSE file for details.