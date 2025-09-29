import json
from dataclasses import dataclass
from typing import Any, Dict, Union

from notihub.notifiers.aws.clients.base_aws_client import BaseAWSClient



@dataclass
class SNSClient(BaseAWSClient):
    """
    SNSClient

    Class used to generate notifications via AWS SNS
    """

    def __post_init__(self):
        self.sns_client = self.initialize_client("sns")

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
            \*args: Additional arguments
            \*\*kwargs: Additional keyword arguments

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
            \*\*kwargs: Additional keyword arguments

        Returns:
            dict: Response of the client operation
        """
        return self.sns_client.publish(
            PhoneNumber=phone_number,
            Message=message,
            **kwargs,
        )

    def send_push_notification(
        self,
        device: str,
        message: str,
        title: str,
        payload: Union[Dict[str, Any], None] = None,
        **kwargs,
    ) -> str:
        """
        Sends a push notification with a title to the given message

        Args:
            device (str): The device to send the message to
            title (str): The title of the push notification
            message (str): The message to send
            payload (dict, optional): Custom payload to send. If not provided,
            a default will be used.

        Returns:
            dict: Response of the client operation
        """
        if payload is None:
            payload = {
                "default": message,
                "APNS": json.dumps({"aps": {"alert": {"title": title, "body": message}}}),
                "APNS_SANDBOX": json.dumps(
                    {"aps": {"alert": {"title": title, "body": message}}}
                ),
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
            platform_application_arn (str): The ARN of the platform application
            (e.g., APNS).
            device_token (str): The token associated with the device to register.
            custom_user_data (str, optional): The custom user data to associate with the
            device endpoint. This should be a JSON-formatted string
            representing user-specific data, such as user ID, subscription type, etc.
            If not provided, no custom user data is associated with the endpoint.
            Defaults to "".

        Returns:
            dict: Response from the SNS client operation,
                which includes the platform endpoint details
                or an error message if the operation fails.
        """
        response = self.sns_client.create_platform_endpoint(
            PlatformApplicationArn=platform_application_arn,
            Token=device_token,
            CustomUserData=custom_user_data,
        )

        return response

    def delete_device_endpoint(self, endpoint_arn: str, **kwargs) -> dict:
        """
        Deletes the platform endpoint for the given endpoint ARN.
        Args:
            endpoint_arn (str): The ARN of the platform endpoint to delete.
        Returns:
            dict: Response from the SNS client operation, which includes the result of
            the delete operation or an error message if the operation fails.
        """
        response = self.sns_client.delete_endpoint(EndpointArn=endpoint_arn)
        return response

    def update_device_endpoint(
        self, endpoint_arn: str, custom_user_data: str = "", **kwargs
    ) -> dict:
        """
        Updates the CustomUserData for the given platform endpoint.
        Args:
            endpoint_arn (str): The ARN of the platform endpoint to update.
            custom_user_data (str): The new custom user data to
            associate with the endpoint.
                This should be a JSON-formatted string representing user-specific data.
        Returns:
            dict: Response from the SNS client operation, which includes the
            updated platform endpoint details or an error message if the operation fails.
        """
        response = self.sns_client.set_endpoint_attributes(
            EndpointArn=endpoint_arn, Attributes={"CustomUserData": custom_user_data}
        )
        return response
