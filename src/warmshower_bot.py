class WarmshowerBot:
    """Constructs the welcome message."""

    # Message blocks https://api.slack.com/tools/block-kit-builder?mode=message&blocks=%5B%5D

    def __init__(self, channel: str):
        self.channel = channel
        self.username = "warmshowerbot"
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""

    def get_message_payload(self, user_name: str):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Hi {}! :wave:".format(user_name)
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "I'm here to help you with leaving some warm words about your colleagues right here within Slack. These are just a few things which you will be able to do:"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "• Praise your colleagues anonymously with the command `/praise <username>` \n • Show all praise submitted for you with the command `/praise` \n • Get notified about a new praise for you"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Go ahead and try out one of the commands listed above! :grinning:"
                    }
                }
            ]
        }