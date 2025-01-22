"""

AWS Notifier

This module contains the AWS notifier class which is used to send notifications via AWS
SNS or SES
"""

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Type

import boto3

from notihub.base_notifier import BaseNotifier


@dataclass
class AWSNotifier(BaseNotifier):
    """
    AWSNotifier

    Class used to generate notifications via AWS SNS or SES
    """

    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str

    def __post_init__(self):
        """Initializes the AWS notifier"""
        self.sns_client = self.create_client("sns")
        self.ses_client = self.create_client("ses")

    def create_client(self, service_name: str) -> Type[boto3.client]:
        """
        Creates a client for the given service

        Args:
            service_name (str): The name of the service [sns, ses]

        Returns:
            boto3.client: The client
        """
        return boto3.client(
            service_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name,
        )

    def get_topic(self, topic_arn: str) -> Dict[str, Any]:
        """
        Gets a topic with the given ARN

        Args:
            topic_arn (str): The ARN of the topic

        Returns:
            dict: Response of the client operation
        """
        return self.sns_client.get_topic_attributes(TopicArn=topic_arn)

    def delete_topic(self, topic_arn: str) -> Dict[str, Any]:
        """
        Deletes a topic with the given ARN

        Args:
            topic_arn (str): The ARN of the topic

        Returns:
            dict: Response of the client operation
        """
        return self.sns_client.delete_topic(TopicArn=topic_arn)

    def create_topic(self, topic_name: str) -> Dict[str, Any]:
        """
        Creates a topic with the given name

        Args:
            topic_name (str): The name of the topic

        Returns:
            dict: response of the client operation with the ARN of the topic
        """
        return self.sns_client.create_topic(
            Name=topic_name,
        )

    def subscribe_to_topic(
        self, topic_arn: str, protocol: str, endpoint: str
    ) -> Dict[str, Any]:
        """
        Subscribes the given endpoint to the given topic

        Args:
            topic_arn (str): The topic ARN
            protocol (str): The protocol to use
            endpoint (str): The endpoint to subscribe to

        Returns:
            dict: response of the client operation with the ARN of the subscription
        """
        return self.sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol=protocol,
            Endpoint=endpoint,
        )

    def send_topic_notification(
        self,
        *,
        topic_arn: str,
        message: str,
        subject: str,
        message_structure: str = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """

        Sends a notification to the given topic

        Args:
            topic_arn (str): The topic ARN
            message (str): The message to send

        Additional arguments:
            subject (str): The subject of the message
            target_arn (str): The target ARN
            message_structure (str): The message structure
            *args: Additional arguments
            **kwargs: Additional keyword arguments

        Returns:
            dict: Response of the client operation
        """
        return self.sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject,
            MessageStructure=message_structure or "",
            **kwargs,
        )

    def send_sms_notification(
        self, phone_number: str, message: str, **kwargs
    ) -> Dict[str, Any]:
        """
        Sends a SMS notification to the given phone number

        Args:
            phone_number (str): The phone number to send the message to
            message (str): The message to send

        Additional arguments:
            **kwargs: Additional keyword arguments

        Returns:
            dict: Response of the client operation
        """
        return self.sns_client.publish(
            PhoneNumber=phone_number,
            Message=message,
        )

    def create_email_template(
        self, template_name: str, subject: str, text_body: str, html_body: str
    ) -> Dict[str, Any]:
        """
        Creates an email template with the given name

        Args:
            template_name (str): The name of the template
            subject (str): The subject of the template
            text_body (str): The text body of the template
            html_body (str): The HTML body of the template

        Returns:
            dict: Response of the client operation
        """
        return self.ses_client.create_template(
            Template={
                "TemplateName": template_name,
                "SubjectPart": subject,
                "HtmlPart": html_body,
                "TextPart": text_body,
            }
        )

    def update_email_template(
        self, template_name: str, subject: str, text_body: str, html_body: str
    ) -> str:
        """
        Updates an email template with the given name

        Args:
            template_name (str): The name of the template
            subject (str): The subject of the template
            text_body (str): The text body of the template
            html_body (str): The HTML body of the template

        Returns:
            dict: Response of the client operation
        """
        return self.ses_client.update_template(
            Template={
                "TemplateName": template_name,
                "SubjectPart": subject,
                "HtmlPart": html_body,
                "TextPart": text_body,
            }
        )

    def get_email_template(self, template_name: str) -> Dict[str, Any]:
        """
        Gets an email template with the given name

        Args:
            template_name (str): The name of the template

        Returns:
            dict: Response with the template data
        """
        return self.ses_client.get_template(
            TemplateName=template_name,
        )

    def delete_email_template(self, template_name: str) -> Dict[str, Any]:
        """
        Deletes an email template with the given name

        Args:
            template_name (str): The name of the template

        Returns:
            dict: Response of the client operation
        """
        return self.ses_client.delete_template(
            TemplateName=template_name,
        )

    def list_email_templates(self) -> List[Dict[str, Any]]:
        """
        Lists all email templates

        Args:
            template_name (str): The name of the template

        Returns:
            list: List of email templates
        """
        return self.ses_client.list_templates()

    def send_email_notification(
        self,
        *,
        email_data: dict,
        recipients: List[str],
        sender: str,
        template: str,
        cc_emails: List[str] = None,
        bcc_emails: List[str] = None,
        subject: str = None,
        **kwargs,
    ) -> str:
        """

        Sends an email notification to the given emails with a template

        Args:
            email_data (dict): The data to be used in the email template
            recipients (List[str]): The recipients of the email
            sender (str): The sender of the email
            template (str): The name of the email template

        Additional arguments:
            subject (str): The subject of the email (not required if template is provided)
            cc_emails (List[str]): The CC emails of the email
            bcc_emails (List[str]): The BCC emails of the email
            *args: Additional arguments
            **kwargs: Additional keyword arguments

        Returns:
            dict: Response of the client operation
        """
        # If subject is provided the template subject is updated
        if subject:
            template_data = self.get_email_template(template_name=template)
            self.update_email_template(
                template_name=template,
                subject=subject,
                text_body=template_data["Template"].get("TextPart"),
                html_body=template_data["Template"].get("HtmlPart"),
            )

        return self.ses_client.send_templated_email(
            Source=sender,
            Destination={
                "ToAddresses": recipients,
                "CcAddresses": cc_emails or [],
                "BccAddresses": bcc_emails or [],
            },
            Template=template,
            TemplateData=json.dumps(email_data),
        )

    def send_push_notification(
        self,
        device: str,
        message: str,
        title: str,
        payload: dict = None,
        **kwargs,
    ) -> str:
        """
        Sends a push notification with a title to the given message

        Args:
            device (str): The device to send the message to
            title (str): The title of the push notification
            message (str): The message to send
            payload (dict, optional): Custom payload to send. If not provided, a default will be used.

        Returns:
            dict: Response of the client operation
        """
        if payload is None:
            # Use default payload structure
            payload = {
                "default": message,
                "APNS": json.dumps({"aps": {"alert": {"title": title, "body": message}}}),
                "APNS_SANDBOX":json.dumps({"aps": {"alert": {"title": title, "body": message}}}),
                "GCM": json.dumps({"notification": {"title": title, "body": message}}),
            }

        return self.sns_client.publish(
            TargetArn=device, Message=json.dumps(payload), MessageStructure="json"
        )
    


    def create_device_endpoint(
        self,
        platform_application_arn: str,
        device_token: str,
        custom_user_data: str = "",
        **kwargs,
    ):
        """
        Creates a platform endpoint for the given device token.
        Args:
            platform_application_arn (str): The ARN of the platform application (e.g., APNS).
            device_token (str): The token associated with the device to register.
            custom_user_data (str, optional): The custom user data to associate with the device endpoint.
                This should be a JSON-formatted string representing user-specific data, such as user ID,
                subscription type, etc. If not provided, no custom user data is associated with the endpoint.
                Defaults to "".
        Returns:
            dict: Response from the SNS client operation, which includes the platform endpoint details
                or an error message if the operation fails.
        """
        try:

            response = self.sns_client.create_platform_endpoint(
                PlatformApplicationArn=platform_application_arn,
                Token=device_token,
                CustomUserData=custom_user_data,
            )

            return response
        except Exception as e:
            return {str(e)}

    def delete_device_endpoint(self, endpoint_arn: str, **kwargs) -> dict:
        """
        Deletes the platform endpoint for the given endpoint ARN.
        Args:
            endpoint_arn (str): The ARN of the platform endpoint to delete.
        Returns:
            dict: Response from the SNS client operation, which includes the result of the delete operation
                or an error message if the operation fails.
        """
        try:
            response = self.sns_client.delete_endpoint(EndpointArn=endpoint_arn)
            return response
        except Exception as e:
            return {str(e)}

    def update_device_endpoint(
        self, endpoint_arn: str, custom_user_data: str = "", **kwargs
    ) -> dict:
        """
        Updates the CustomUserData for the given platform endpoint.
        Args:
            endpoint_arn (str): The ARN of the platform endpoint to update.
            custom_user_data (str): The new custom user data to associate with the endpoint.
                This should be a JSON-formatted string representing user-specific data.
        Returns:
            dict: Response from the SNS client operation, which includes the updated platform endpoint details
                or an error message if the operation fails.
        """
        try:

            response = self.sns_client.set_endpoint_attributes(
                EndpointArn=endpoint_arn, Attributes={"CustomUserData": custom_user_data}
            )
            return response
        except Exception as e:
            return {str(e)}
