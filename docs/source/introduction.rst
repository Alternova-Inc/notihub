Introduction
============

Overview
--------

NotiHub is a Python library designed to manage and use different notification services through a unified, plug-and-play interface. The library's core philosophy centers around providing a consistent abstraction layer over various notification providers, allowing developers to switch between services or use multiple providers simultaneously with minimal code changes.

Plug-and-Play Design Philosophy
-------------------------------

The plug-and-play design philosophy of NotiHub offers several key benefits:

*   **Consistency**: All notification providers implement the same interface, ensuring consistent behavior across different services.
*   **Flexibility**: Easy to add new notification providers or switch between existing ones without changing application code.
*   **Maintainability**: Centralized configuration and error handling reduces code duplication.
*   **Extensibility**: Simple to extend functionality for new notification channels or providers.
*   **Testability**: Consistent interfaces make unit testing straightforward and provider-agnostic.

Quick Start
-----------

Install NotiHub using pip:

.. code-block:: bash

    pip install notihub

Basic usage with AWS:

.. code-block:: python

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

Basic usage with Twilio:

.. code-block:: python

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