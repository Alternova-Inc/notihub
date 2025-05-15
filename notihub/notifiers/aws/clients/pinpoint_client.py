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
        aps_payload = {"sound": "default"}

        if silent_push:
            aps_payload["content-available"] = 1
        else:
            aps_payload["alert"] = {"title": title, "body": body}

        if image_url:
            aps_payload["mutable-content"] = 1

        payload_root = {"aps": aps_payload, **custom_data}
        message = {
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
        payload_data = {**custom_data, "title": title, "body": body}

        gcm_payload = {"data": payload_data}
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

        message = {
            "Action": action,
            "RawContent": json.dumps(gcm_payload),
        }
        if deep_link_url:
            message["Url"] = deep_link_url

        return message

    def _build_default_message(
        self,
        *,
        title: str,
        body: str,
        action: str,
        deep_link_url: Optional[str],
    ) -> Dict[str, Any]:
        """Build the default message."""
        message = {"Action": action, "Title": title, "Body": body}
        if deep_link_url:
            message["Url"] = deep_link_url

        return message

    def send_pinpoint_push_notification(
        self,
        *,
        application_id: str,
        endpoint_ids: List[str],
        title: str,
        body: str,
        deep_link_url: Optional[str] = None,
        image_url: Optional[str] = None,
        custom_data: Optional[Dict[str, Any]] = None,
        silent_push: bool = False,
        time_to_live: Optional[int] = None,
        priority: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Sends a push notification via Pinpoint to specified endpoints.
        """
        action = "DEEP_LINK" if deep_link_url else "OPEN_APP"
        processed_custom_data = self._prepare_custom_data(
            custom_data, deep_link_url=deep_link_url, image_url=image_url
        )
        apns_message = self._build_apns_message(
            title=title,
            body=body,
            action=action,
            deep_link_url=deep_link_url,
            image_url=image_url,
            silent_push=silent_push,
            custom_data=processed_custom_data,
        )
        gcm_message = self._build_gcm_message(
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
        default_message = self._build_default_message(
            title=title,
            body=body,
            action=action,
            deep_link_url=deep_link_url,
        )
        message_request = {
            "Endpoints": {endpoint_id: {} for endpoint_id in endpoint_ids},
            "MessageConfiguration": {
                "APNSMessage": apns_message,
                "GCMMessage": gcm_message,
                "DefaultPushNotificationMessage": default_message,
            },
        }
        response = self.pinpoint_client.send_messages(
            ApplicationId=application_id, MessageRequest=message_request
        )
        return response

    def get_pinpoint_endpoint(
        self, application_id: str, endpoint_id: str
    ) -> Dict[str, Any]:
        """
        Get a specific Pinpoint endpoint.

        Args:
            application_id: The Pinpoint Application ID.
            endpoint_id: The unique identifier of the endpoint to get.

        Returns:
            The response from the Pinpoint get_endpoint operation.
        """
        try:
            return self.pinpoint_client.get_endpoint(
                ApplicationId=application_id, EndpointId=endpoint_id
            )
        except self.pinpoint_client.exceptions.NotFoundException as e:
            return {"error": e.response["Error"]["Message"]}

    def get_pinpoint_user_endpoints(
        self, application_id: str, user_id: str
    ) -> Dict[str, Any]:
        """
        Get all Pinpoint endpoints for a specific user.
        """
        try:
            return self.pinpoint_client.get_user_endpoints(
                ApplicationId=application_id, UserId=user_id
            )
        except self.pinpoint_client.exceptions.NotFoundException as e:
            return {"error": e.response["Error"]["Message"]}
