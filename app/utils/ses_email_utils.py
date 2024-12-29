import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError

def send_email_ses(
    sender: str,
    recipient: str,
    subject: str,
    body_text: str,
    body_html: str = "",
    region_name: str = "us-east-1"
) -> bool:
    """
    Send an email using AWS SES.
    - Make sure 'sender' is a verified email or domain in SES.
    - If your account is in the SES sandbox, 'recipient' must also be verified.
    - region_name should match your configured SES region.
    - AWS credentials must be set in environment variables or a secure location.

    Returns True if successful, False otherwise.
    """
    ses_client = boto3.client("ses", region_name=region_name)
    
    try:
        response = ses_client.send_email(
            Source=sender,
            Destination={
                "ToAddresses": [recipient],
            },
            Message={
                "Subject": {"Data": subject, "Charset": "UTF-8"},
                "Body": {
                    "Text": {"Data": body_text, "Charset": "UTF-8"},
                    "Html": {"Data": body_html, "Charset": "UTF-8"},
                },
            },
        )
        print("Email sent! Message ID:", response["MessageId"])
        return True
    except (BotoCoreError, ClientError) as e:
        print("Error sending email via SES:", str(e))
        return False