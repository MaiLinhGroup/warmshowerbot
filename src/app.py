import json
import logging
import os
import re

from dotenv import load_dotenv
from flask import Flask, request, make_response
from slack import WebClient
from slack.errors import SlackApiError
from slackeventsapi import SlackEventAdapter
from src.database import database as db
from src.warmshower_bot import WarmshowerBot

load_dotenv(verbose=True)
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)
slack_web_client = WebClient(token=SLACK_BOT_TOKEN)

warmshower_bot_sent = {}


@app.route("/praise", methods=["POST"])
def praise():
    reply = ""
    text = request.form.get("text")
    x = re.search("@[\w.]+", text)
    if x is not None:
        user_id = x.group()[1:]
        try:
            user_name = slack_web_client.users_info(user=user_id)["user"]["real_name"]
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # "user_not_found"
            logger.debug(e)
            reply = "Sorry, I don't know this user :( "
        else:
            db.add_user(user_id, user_name)
            reply = "Ok let's write some warm words for {} :)".format(user_name)
    else:
        reply = "Sorry, can you try again with `/praise <@username>`?"
    return reply, 200


def start_warmshower(user_id: str, channel: str):
    # Create a warmshower bot
    warmshower_bot = WarmshowerBot(channel)

    user_name = slack_web_client.users_info(user=user_id)["user"]["real_name"]

    # Get the message payload
    msg_payload = warmshower_bot.get_message_payload(user_name)

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
    """Display the welcome message after receiving a direct message
    that contains "start".
    """
    event = payload.get("event", {})

    # Filter for DM with app only
    if event.get("channel_type") != "im":
        return

    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")

    if text and text.lower() == "start":
        return start_warmshower(user_id, channel_id)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(host="0.0.0.0", port=80)
