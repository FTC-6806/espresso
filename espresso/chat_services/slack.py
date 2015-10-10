import json

from slackclient import SlackClient
from ..user import User

class SlackChatAdaptor(object):
	def __init__(self, config):
		self.config = config
		self.api_token = config['api_token']
		self._bot_user = None
		self.slack_client = None

	def connect(self):
		self.slack_client = SlackClient(self.api_token)
		self.slack_client.rtm_connect()

		# test auth and grab the current user
		slack_test = json.loads(self.slack_client.api_call('auth.test'))
		self._bot_user = User(slack_test['user_id'], slack_test['user'])

	@property
	def bot_user(self):
	    return self._bot_user

	@property
	def wrapped_client(self):
	    return self.slack_client

	def read_stream(self):
		return self.slack_client.rtm_read()

	def send(self, message, channel):
		"""Send a message to slack"""
		self.slack_client.server.channels.find(channel).send_message(message)