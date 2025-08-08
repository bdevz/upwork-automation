"""
Slack notification utility to send messages to a specified channel.
"""
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.errors import SlackApiError

from shared.config import settings
from shared.logger import logger


async def send_slack_notification(channel: str, message: str):
    """
    Sends a notification to a Slack channel.
    """
    client = AsyncWebClient(token=settings.slack_bot_token)
    try:
        await client.chat_postMessage(channel=channel, text=message)
        logger.info(f"Sent Slack notification to channel {channel}")
    except SlackApiError as e:
        logger.error(f"Error sending Slack notification: {e.response['error']}")


class Notification(object):
