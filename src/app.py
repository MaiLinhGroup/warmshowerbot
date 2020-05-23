import logging
import os

from dotenv import load_dotenv
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from warmshower_bot import WarmshowerBot

load_dotenv(verbose=True)
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)
slack_web_client = WebClient(token=SLACK_BOT_TOKEN)

# TODO: replace in-mem storage with sqlite db
warmshower_bot_sent = {}

@app.route('/<name>')
def hello(name: str) -> str:
    return "Hello {}!".format(name)

def start_warmshower(user_id: str, channel: str):
    # Create a warmshower bot
    warmshower_bot = WarmshowerBot(channel)

    # Get the message payload
    msg_payload = warmshower_bot.get_message_payload()

    # Post the welcome message in Slack
    response = slack_web_client.chat_postMessage(**msg_payload)

    # Capture timestamp of message to update it later
    warmshower_bot.timestamp = response["ts"]

    # Store message sent in-memory
    if channel not in warmshower_bot_sent:
        warmshower_bot_sent[channel] = {}
    warmshower_bot_sent[channel][user_id] = warmshower_bot

# ============== Message Events ============= #
# When a user sends a DM, the event type will be 'message'.
# Here we'll link the message callback to the 'message' event.
@slack_events_adapter.on("message")
def event_message(payload):
    """Display the welcome message after receiving a message
    that contains "start".
    """
    event = payload.get("event", {})

    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")

    if text and text.lower() == "start":
        return start_warmshower(user_id, channel_id)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(host='0.0.0.0', port=8080)