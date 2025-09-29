import json
from dataclasses import dataclass
from typing import Any, Dict, List, ClassVar

from notihub.notifiers.aws.clients.base_aws_client import BaseAWSClient


@dataclass
class SESClient(BaseAWSClient):
    """
    SESClient

    Class used to generate notifications via AWS SES
    """
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str

    def __post_init__(self):
        self.ses_client = self.initialize_client("ses")

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
            \*args: Additional arguments
            \*\*kwargs: Additional keyword arguments

        Returns:
            dict: Response of the client operation
        """
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
            **kwargs,
        )
