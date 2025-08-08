"""
Utility functions for sending notifications, initially supporting Slack.
"""
from slack_sdk.webhook import WebhookClient

from shared.config import settings
from shared.logger import logger


def send_slack_notification(message: str, webhook_url: str = None):
    """
    Sends a notification to a Slack channel using a webhook.

    Args:
        message (str): The message to send.
        webhook_url (str, optional): The Slack webhook URL. If not provided,
                                     it will be read from settings.
    """
    if not webhook_url:
        webhook_url = settings.n8n_webhook_url

    if not webhook_url:
        logger.warning("Slack webhook URL is not configured. Skipping notification.")
        return

    webhook = WebhookClient(webhook_url)
    response = webhook.send(text=message)

    if response.status_code != 200:
        logger.error(
            "Failed to send Slack notification. Status: %s, Body: %s",
            response.status_code,
            response.body,
        )
