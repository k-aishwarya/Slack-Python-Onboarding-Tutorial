# -*- coding: utf-8 -*-
"""
Python Slack Bot class for use with the pythOnBoarding app
"""
import os
# import message

from slackclient import SlackClient

# To remember which teams have authorized your app and what tokens are
# associated with each team, we can store this information in memory on
# as a global object. When your bot is out of development, it's best to
# save this in a more persistent memory store.
authed_teams = {}


class Bot(object):
    """ Instantiates a Bot object to handle Slack onboarding interactions."""
    def __init__(self):
        super(Bot, self).__init__()
        self.name = "pythonboardingbot"
        self.emoji = ":robot_face:"
        # When we instantiate a new bot object, we can access the app
        # credentials we set earlier in our local development environment.
        self.oauth = {"client_id": "316442097986.1329524380803",
                      "client_secret": "0594580f3e790d5d6fb5a0c9fd186e62",
                      # Scopes provide and limit permissions to what our app
                      # can access. It's important to use the most restricted
                      # scope that your app will need.
                      "scope": "bot"}
        self.verification = "LslojzHwgCLEoxu97IvZWWvD"

        # NOTE: Python-slack requires a client connection to generate
        # an OAuth token. We can connect to the client without authenticating
        # by passing an empty string as a token and then reinstantiating the
        # client with a valid OAuth token once we have one.
        self.client = SlackClient("xoxb-316442097986-1329534361827-NK3yPsReBnwiAaJoJF39D4H3")
        # We'll use this dictionary to store the state of each message object.
        # In a production environment you'll likely want to store this more
        # persistently in  a database.
        self.messages = {}

    def auth(self, code):
        """
        Authenticate with OAuth and assign correct scopes.
        Save a dictionary of authed team information in memory on the bot
        object.

        Parameters
        ----------
        code : str
            temporary authorization code sent by Slack to be exchanged for an
            OAuth token

        """
        # After the user has authorized this app for use in their Slack team,
        # Slack returns a temporary authorization code that we'll exchange for
        # an OAuth token using the oauth.access endpoint
        auth_response = self.client.api_call(
                                "oauth.access",
                                client_id=self.oauth["client_id"],
                                client_secret=self.oauth["client_secret"],
                                code=code
                                )
        # To keep track of authorized teams and their associated OAuth tokens,
        # we will save the team ID and bot tokens to the global
        # authed_teams object
        team_id = auth_response["team_id"]
        authed_teams[team_id] = {"bot_token":
                                 auth_response["bot"]["bot_access_token"]}
        # Then we'll reconnect to the Slack Client with the correct team's
        # bot token
        self.client = SlackClient(authed_teams[team_id]["bot_token"])

    # def open_dm(self, user_id):
    #     """
    #     Open a DM to send a welcome message when a 'team_join' event is
    #     recieved from Slack.

    #     Parameters
    #     ----------
    #     user_id : str
    #         id of the Slack user associated with the 'team_join' event

    #     Returns
    #     ----------
    #     dm_id : str
    #         id of the DM channel opened by this method
    #     """
    #     new_dm = self.client.api_call("im.open",
    #                                   user=user_id)
    #     dm_id = new_dm["channel"]["id"]
    #     return dm_id

    # def onboarding_message(self, team_id, user_id):
    #     """
    #     Create and send an onboarding welcome message to new users. Save the
    #     time stamp of this message on the message object for updating in the
    #     future.

    #     Parameters
    #     ----------
    #     team_id : str
    #         id of the Slack team associated with the incoming event
    #     user_id : str
    #         id of the Slack user associated with the incoming event

    #     """
    #     # We've imported a Message class from `message.py` that we can use
    #     # to create message objects for each onboarding message we send to a
    #     # user. We can use these objects to keep track of the progress each
    #     # user on each team has made getting through our onboarding tutorial.

    #     # First, we'll check to see if there's already messages our bot knows
    #     # of for the team id we've got.
    #     if self.messages.get(team_id):
    #         # Then we'll update the message dictionary with a key for the
    #         # user id we've received and a value of a new message object
    #         self.messages[team_id].update({user_id: message.Message()})
    #     else:
    #         # If there aren't any message for that team, we'll add a dictionary
    #         # of messages for that team id on our Bot's messages attribute
    #         # and we'll add the first message object to the dictionary with
    #         # the user's id as a key for easy access later.
    #         self.messages[team_id] = {user_id: message.Message()}
    #     message_obj = self.messages[team_id][user_id]
    #     # Then we'll set that message object's channel attribute to the DM
    #     # of the user we'll communicate with
    #     message_obj.channel = self.open_dm(user_id)
    #     # We'll use the message object's method to create the attachments that
    #     # we'll want to add to our Slack message. This method will also save
    #     # the attachments on the message object which we're accessing in the
    #     # API call below through the message object's `attachments` attribute.
    #     message_obj.create_attachments()
    #     post_message = self.client.api_call("chat.postMessage",
    #                                         channel=message_obj.channel,
    #                                         username=self.name,
    #                                         icon_emoji=self.emoji,
    #                                         text=message_obj.text,
    #                                         attachments=message_obj.attachments
    #                                         )
    #     timestamp = post_message["ts"]
    #     # We'll save the timestamp of the message we've just posted on the
    #     # message object which we'll use to update the message after a user
    #     # has completed an onboarding task.
    #     message_obj.timestamp = timestamp

    # def update_emoji(self, team_id, user_id):
    #     """
    #     Update onboarding welcome message after recieving a "reaction_added"
    #     event from Slack. Update timestamp for welcome message.

    #     Parameters
    #     ----------
    #     team_id : str
    #         id of the Slack team associated with the incoming event
    #     user_id : str
    #         id of the Slack user associated with the incoming event

    #     """
    #     # These updated attachments use markdown and emoji to mark the
    #     # onboarding task as complete
    #     completed_attachments = {"text": ":white_check_mark: "
    #                                      "~*Add an emoji reaction to this "
    #                                      "message*~ :thinking_face:",
    #                              "color": "#439FE0"}
    #     # Grab the message object we want to update by team id and user id
    #     message_obj = self.messages[team_id].get(user_id)
    #     # Update the message's attachments by switching in incomplete
    #     # attachment with the completed one above.
    #     message_obj.emoji_attachment.update(completed_attachments)
    #     # Update the message in Slack
    #     post_message = self.client.api_call("chat.update",
    #                                         channel=message_obj.channel,
    #                                         ts=message_obj.timestamp,
    #                                         text=message_obj.text,
    #                                         attachments=message_obj.attachments
    #                                         )
    #     # Update the timestamp saved on the message object
    #     message_obj.timestamp = post_message["ts"]

    # def update_pin(self, team_id, user_id):
    #     """
    #     Update onboarding welcome message after receiving a "pin_added"
    #     event from Slack. Update timestamp for welcome message.

    #     Parameters
    #     ----------
    #     team_id : str
    #         id of the Slack team associated with the incoming event
    #     user_id : str
    #         id of the Slack user associated with the incoming event

    #     """
    #     # These updated attachments use markdown and emoji to mark the
    #     # onboarding task as complete
    #     completed_attachments = {"text": ":white_check_mark: "
    #                                      "~*Pin this message*~ "
    #                                      ":round_pushpin:",
    #                              "color": "#439FE0"}
    #     # Grab the message object we want to update by team id and user id
    #     message_obj = self.messages[team_id].get(user_id)
    #     # Update the message's attachments by switching in incomplete
    #     # attachment with the completed one above.
    #     message_obj.pin_attachment.update(completed_attachments)
    #     # Update the message in Slack
    #     post_message = self.client.api_call("chat.update",
    #                                         channel=message_obj.channel,
    #                                         ts=message_obj.timestamp,
    #                                         text=message_obj.text,
    #                                         attachments=message_obj.attachments
    #                                         )
    #     # Update the timestamp saved on the message object
    #     message_obj.timestamp = post_message["ts"]

    def update_share(self, team_id, user_id, ts, message_body):
        """
        Update onboarding welcome message after recieving a "message" event
        with an "is_share" attachment from Slack. Update timestamp for
        welcome message.

        Parameters
        ----------
        team_id : str
            id of the Slack team associated with the incoming event
        user_id : str
            id of the Slack user associated with the incoming event

        """
        print("update_share")
        attachments_json = [
            {
                "fallback": "Upgrade your Slack client to use messages like these.",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "callback_id": "menu_options_2319",
                "actions": [
                    {
                        "name": "bev_list",
                        "text": "Pick a beverage...",
                        "type": "select",
                        "data_source": "external"
                    }
                ]
            }
        ]

        # Send a message with the above attachment, asking the user if they want coffee
        if(message_body=="hello"):
            self.client.api_call(
            "chat.postMessage",
            channel="grant-test-1",
            text="Would you like some coffee? :coffee:",
            attachments=attachments_json,
            thread_ts=ts
            )

        # if(message_body=="hello"):
        #     self.client.api_call(
        #         "chat.postMessage",
        #         channel="grant-test-1",
        #         text="Test Message",
        #         thread_ts=ts
        #     )

    def update_chat(self,form_json):
        print("update_chat")
        # Check to see what the user's selection was and update the message
        selection = form_json["actions"][0]["selected_options"][0]["value"]

        if selection == "war":
            message_text = "The only winning move is not to play.\nHow about a nice game of chess?"
        else:
            message_text = ":horse:"

        self.client.api_call(
            "chat.update",
            channel=form_json["channel"]["id"],
            ts=form_json["message_ts"],
            text=message_text,
            attachments=[]
            )

