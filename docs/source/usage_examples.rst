Usage Examples
==============

Comprehensive code examples for using AWS and Twilio notifiers.

AWS Notifier Usage
------------------

.. code-block:: python

    from notihub.client import NotifierClient

    # Initialize AWS notifier
    aws_notifier = NotifierClient.get_aws_notifier(
        aws_access_key_id="your_access_key",
        aws_secret_access_key="your_secret_key",
        region_name="us-east-1"
    )

    # Send SMS via AWS SNS
    sms_result = aws_notifier.send_sms_notification(
        phone_number="+1234567890",
        message="Hello from NotiHub!"
    )

    # Send email via AWS SES
    email_result = aws_notifier.send_email_notification(
        subject="Test Email",
        email_data={"name": "John Doe", "content": "This is a test email"},
        recipients=["john@example.com"],
        sender="noreply@yourapp.com",
        template="welcome_template"
    )

    # Send push notification via AWS SNS
    push_result = aws_notifier.send_push_notification(
        device="arn:aws:sns:us-east-1:123456789012:endpoint/APNS_SANDBOX/...",
        message="You have a new notification!",
        title="NotiHub Alert"
    )

Twilio Notifier Usage
---------------------

.. code-block:: python

    from notihub.client import NotifierClient

    # Initialize Twilio notifier
    twilio_notifier = NotifierClient.get_twilio_notifier(
        account_sid="your_account_sid",
        auth_token="your_auth_token",
        twilio_phone_number="+1234567890"
    )

    # Send SMS via Twilio
    sms_result = twilio_notifier.send_sms_notification(
        phone_number="+0987654321",
        message="Hello from Twilio via NotiHub!"
    )

Error Handling and Best Practices
---------------------------------

.. code-block:: python

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