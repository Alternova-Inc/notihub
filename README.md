# NotiHub - Plug-and-Play Notification Library

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A unified, plug-and-play solution for sending notifications through various providers.

## Introduction

NotiHub is a Python library designed to manage and use different notification services through a unified, plug-and-play interface. The library's core philosophy centers around providing a consistent abstraction layer over various notification providers, allowing developers to switch between services or use multiple providers simultaneously with minimal code changes.

### Why NotiHub?

The plug-and-play design philosophy of NotiHub offers several key benefits:

*   **Consistency**: All notification providers implement the same interface, ensuring consistent behavior across different services.
*   **Flexibility**: Easy to add new notification providers or switch between existing ones without changing application code.
*   **Maintainability**: Centralized configuration and error handling reduces code duplication.
*   **Extensibility**: Simple to extend functionality for new notification channels or providers.
*   **Testability**: Consistent interfaces make unit testing straightforward and provider-agnostic.

## Quick Start

Install NotiHub using pip:

```bash
pip install notihub
```

Basic usage with AWS:

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
```

## Core Concepts

### BaseNotifier Abstract Class

The `BaseNotifier` abstract class serves as the foundation for all notification providers in NotiHub. It defines the standard interface that all notifiers must implement, ensuring consistency across different services.

All notifiers in NotiHub inherit from the `BaseNotifier` abstract class, which defines three core methods:

*   `send_sms_notification()`: For sending SMS messages
*   `send_email_notification()`: For sending email notifications
*   `send_push_notification()`: For sending push notifications

This abstraction allows developers to write code that works with any supported notification provider without modification.

## Supported Notifiers

NotiHub currently supports the following notification providers:

### AWS Notifier

The AWS notifier provides integration with multiple AWS services:

*   **Amazon SNS**: For SMS and push notifications
*   **Amazon SES**: For email notifications
*   **Amazon Pinpoint**: For advanced messaging capabilities

### Twilio Notifier

The Twilio notifier provides integration with Twilio's communication platform, primarily focused on SMS messaging.

## Further Documentation

For complete documentation, including installation instructions, usage examples, API references, and detailed configuration guides, please visit our [Read the Docs documentation](https://notihub.readthedocs.io).

## Contributing

We welcome contributions to NotiHub! Whether you're fixing bugs, adding new features, or improving documentation, your help is appreciated.

Please see our full [contributing guidelines](https://notihub.readthedocs.io/en/latest/contributing.html) for details on our development workflow, code style guidelines, and how to add new providers.
