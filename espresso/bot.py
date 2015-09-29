import imp
import json
import logging
import time

from slackclient import SlackClient

from .brain import Brain
from .listener import Listener
from .listener import ListenerType
from .message import Message
from .repl import EspressoConsole
from .user import User
from .plugin_api import PluginAPI


class Espresso(PluginAPI, object):
    """The bot's main class, responsible for event loop, callbacks, and messaging connection.

    The plugin API's decorators are mixed in to this class.
    """

    def __init__(self, config):
        self.config = config
        self.api_token = config['api_token']
        self.debug = config['debug']
        self.slack_client = None
        self.listeners = []
        self.user = None
        self.brain = Brain(config['brainstate_location'])

    def connect(self):
        """Connects to Slack.

        Creates a new SlackClient with ``self.api_token``.
        """
        # TODO: Refactor for abstract MessagingServices.

        self.slack_client = SlackClient(self.api_token)
        self.slack_client.rtm_connect() # connect to the real-time messaging system

        slack_test = json.loads(self.slack_client.api_call('auth.test'))
        self.user = User(slack_test['user_id'], slack_test['user'])
        logging.info("I am @%s, uid %s", self.user.name, self.user.uid)

    def load_plugins(self, plugins, plugindir):
        """Loads specified plugins from the specified plugin directory.

        Args:
            plugins: plugins to load
            plugindir: directory to load plugins from
        """

        if plugins is not None:
            for plugin in plugins:
                logging.debug('loading plugin %s from %s', plugin, plugindir)

                file_descriptor, path, desc = imp.find_module(plugin, [plugindir])

                try:
                    imp.load_module(plugin, file_descriptor, path, desc)
                finally:
                    if file_descriptor:
                        file_descriptor.close()

    def brew(self):
        """Run the bot.

        Starts an infinite processing/event loop.
        """

        logging.info("starting the bot")
        self.connect()

        self.load_plugins(self.config['plugins'], self.config['plugin_dir'])

        if self.config['debug_console']:
            espresso_console = EspressoConsole(locals())
            espresso_console.interact()

        while True:
            for msg in self.slack_client.rtm_read():
                logging.debug("Raw message: %s", msg)
                if 'type' in msg:
                    if msg['type'] == 'message' and 'subtype' not in msg:
                        message = Message(User(msg['user'],
                                               self.slack_client.server.users.find(msg['user']).name),
                                          self.slack_client.server.channels.find(msg['channel']),
                                          msg['text'])

                        for listener in self.listeners:
                            listener.call(message)

            # sleep for 1/10 sec to not peg the cpu
            # with this basic async implementation
            time.sleep(.1)

    def add_listener(self, ltype, regex, function, options):
        """Adds a listener listening for something from the messaging system.

        Args:
            ltype: the type of the regex.
            regex: a regex string identifying what to listen for.
            function: the callback to call if the regex matches.
            options: a dict of options to pass on.
        """
        if ltype == ListenerType.heard:
            self.listeners.append(Listener(self, regex, function, options))
        elif ltype == ListenerType.heard_with_name:
            regex = r"^(?:\<\@{uid}\>|{uname})\s*:?\s*".format(
                uid=self.user.uid,
                uname=self.user.name) + regex
            self.listeners.append(Listener(self, regex, function, options))

        logging.debug("Added listener of type %s with regex %s calling %s",
                      ltype, regex, function.__name__)

    def send(self, message, channel):
        """Send a message to the messaging system."""

        logging.debug("Send message %s to #%s", message, channel)
        self.slack_client.server.channels.find(channel).send_message(message)
