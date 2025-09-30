Supported Notifiers
===================

NotiHub currently supports the following notification providers:

AWS Notifier
------------

The AWS notifier provides integration with multiple AWS services:

*   **Amazon SNS**: For SMS and push notifications
*   **Amazon SES**: For email notifications
*   **Amazon Pinpoint**: For advanced messaging capabilities

The AWS notifier combines all three services into a single interface, allowing you to send different types of notifications through the most appropriate AWS service.

Twilio Notifier
---------------

The Twilio notifier provides integration with Twilio's communication platform, primarily focused on SMS messaging. Twilio is known for its reliability and global reach for SMS communications.

Note: Twilio does not directly support email or push notifications in this library implementation.