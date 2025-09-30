import uuid
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from notihub.notifiers.aws.clients.base_aws_client import BaseAWSClient


@dataclass
class PinpointAddress:
    """A recipient address for Pinpoint, including token and service."""

    token: str
    service: str


@dataclass
class PinpointClient(BaseAWSClient):
    """
    PinpointClient

    Class used to generate notifications via AWS Pinpoint
    """
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str

    def __post_init__(self):
        self.pinpoint_client = self.initialize_client("pinpoint")

    def _prepare_custom_data(
        self,
        custom_data: Optional[Dict[str, Any]],
        *,
        deep_link_url: Optional[str],
        image_url: Optional[str],
    ) -> Dict[str, Any]:
        """Return a copy of custom_data enriched with deeplink / image_url."""
        data: Dict[str, Any] = (custom_data or {}).copy()
        data.update({"deeplink": deep_link_url, "image_url": image_url})
        return data

    def _build_apns_message(
        self,
        *,
        title: str,
        body: str,
        action: str,
        deep_link_url: Optional[str],
        image_url: Optional[str],
        silent_push: bool,
        custom_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Build the APNS message."""
        aps_payload: Dict[str, Any] = {"sound": "default"}

        if silent_push:
            aps_payload["content-available"] = 1
        else:
            aps_payload["alert"] = {"title": title, "body": body}

        if image_url:
            aps_payload["mutable-content"] = 1

        payload_root = {"aps": aps_payload, **custom_data}
        if deep_link_url:
            payload_root["Url"] = deep_link_url

        message: Dict[str, Any] = {
            "Action": action,
            "RawContent": json.dumps(payload_root),
        }
        if deep_link_url:
            message["Url"] = deep_link_url

        return message

    def _build_gcm_message(
        self,
        *,
        title: str,
        body: str,
        action: str,
        deep_link_url: Optional[str],
        image_url: Optional[str],
        silent_push: bool,
        custom_data: Dict[str, Any],
        time_to_live: Optional[int],
        priority: Optional[str],
    ) -> Dict[str, Any]:
        payload_data = {**custom_data, "title": title, "body": body, "Url": deep_link_url}

        gcm_payload: Dict[str, Any] = {"data": payload_data}
        if silent_push:
            gcm_payload["content_available"] = 1
        else:
            notification = {"title": title, "body": body}
            if image_url:
                notification["image"] = image_url

            gcm_payload["notification"] = notification

        if priority:
            gcm_payload["priority"] = priority

        if time_to_live is not None:
            gcm_payload["time_to_live"] = time_to_live

        message: Dict[str, Any] = {
            "Action": action,
            "RawContent": json.dumps(gcm_payload),
        }
        if deep_link_url:
            message["Url"] = deep_link_url

        return message

    def send_pinpoint_push_notification(
        self,
        *,
        application_id: str,
        addresses: List[PinpointAddress],
        title: str,
        body: str,
        deep_link_url: Optional[str] = None,
        image_url: Optional[str] = None,
        custom_data: Optional[Dict[str, Any]] = None,
        silent_push: bool = False,
        time_to_live: Optional[int] = None,
        priority: Optional[str] = None,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """
        Sends a push notification via Pinpoint to specified addresses.
        It groups addresses by service type (GCM, APNS) and sends a batch for each.
        """
        action = "DEEP_LINK" if deep_link_url else "OPEN_APP"
        processed_custom_data = self._prepare_custom_data(
            custom_data, deep_link_url=deep_link_url, image_url=image_url
        )
        addresses_by_service: Dict[str, List[str]] = {}
        for address in addresses:
            service = address.service.upper()
            if service not in addresses_by_service:
                addresses_by_service[service] = []

            addresses_by_service[service].append(address.token)

        responses = []
        for service, tokens in addresses_by_service.items():
            message_config: Dict[str, Any] = {}
            if service == "GCM":
                message_config["GCMMessage"] = self._build_gcm_message(
                    title=title,
                    body=body,
                    action=action,
                    deep_link_url=deep_link_url,
                    image_url=image_url,
                    silent_push=silent_push,
                    custom_data=processed_custom_data,
                    time_to_live=time_to_live,
                    priority=priority,
                )
            elif service in ["APNS", "APNS_SANDBOX"]:
                message_config["APNSMessage"] = self._build_apns_message(
                    title=title,
                    body=body,
                    action=action,
                    deep_link_url=deep_link_url,
                    image_url=image_url,
                    silent_push=silent_push,
                    custom_data=processed_custom_data,
                )
            else:
                continue

            message_request = {
                "Addresses": {token: {"ChannelType": service} for token in tokens},
                "MessageConfiguration": message_config,
            }
            response = self.pinpoint_client.send_messages(
                ApplicationId=application_id, MessageRequest=message_request
            )
            responses.append(response)

        return responses

    def create_pinpoint_endpoint(
        self,
        *,
        application_id: str,
        device_token: str,
        channel_type: str,
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Creates a new Pinpoint endpoint with a generated unique ID.
        Args:
            application_id: The Pinpoint Application ID.
            device_token: The push notification token from APNS/FCM.
            channel_type: Channel type (e.g., "GCM", "APNS", "APNS_SANDBOX").
            user_id: The user ID of the application.
        Returns:
            Dict containing API response and the generated 'EndpointId'.
            Store the 'EndpointId' for future updates/deletions.
        Raises:
            ClientError: If the Pinpoint API call fails.
        """
        generated_endpoint_id = str(uuid.uuid4())
        endpoint_request: Dict[str, Any] = {
            "Address": device_token,
            "ChannelType": channel_type.upper(),
            "OptOut": "NONE",
        }
        if user_id:
            endpoint_request["UserId"] = user_id

        response = self.pinpoint_client.update_endpoint(
            ApplicationId=application_id,
            EndpointId=generated_endpoint_id,
            EndpointRequest=endpoint_request,
        )
        return {"EndpointId": generated_endpoint_id, **response}

    def update_pinpoint_endpoint(
        self,
        *,
        application_id: str,
        endpoint_id: str,
        device_token: Optional[str] = None,
        channel_type: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Updates specific attributes of an existing Pinpoint endpoint.
        Args:
            application_id: The Pinpoint Application ID.
            endpoint_id: The unique ID of the endpoint to update.
            device_token: Optional new push notification token.
            channel_type: Optional channel type.
            user_id: Optional application's user ID.
        Returns:
            The response from the Pinpoint update_endpoint operation.
        Raises:
            ClientError: If the Pinpoint API call fails.
        """
        endpoint_request: Dict[str, Any] = {}

        if device_token:
            endpoint_request["Address"] = device_token

        if channel_type:
            endpoint_request["ChannelType"] = channel_type.upper()

        if user_id:
            endpoint_request["UserId"] = user_id

        response = self.pinpoint_client.update_endpoint(
            ApplicationId=application_id,
            EndpointId=endpoint_id,
            EndpointRequest=endpoint_request,
        )
        return response

    def delete_pinpoint_endpoint(
        self,
        *,
        application_id: str,
        endpoint_id: str,
    ) -> Dict[str, Any]:
        """Deletes a specific Pinpoint endpoint.
        Args:
            application_id: The Pinpoint Application ID.
            endpoint_id: The unique identifier of the endpoint to delete.
        Returns:
            The response from the Pinpoint delete_endpoint operation.
        Raises:
            ClientError: If the Pinpoint API call fails.
        """
        response = self.pinpoint_client.delete_endpoint(
            ApplicationId=application_id,
            EndpointId=endpoint_id,
        )
        return response
