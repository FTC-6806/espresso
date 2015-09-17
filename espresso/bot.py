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


class Espresso(object):
    """The bot's main class.
    Handles connections and all the things.
    Delegates to plugin files.
    The plugin API is also implemented on the bot, they're all decorators.
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
        """Helper method to connect to Slack.
        Creates a new SlackClient with ``self.api_token``.
        """

        self.slack_client = SlackClient(self.api_token)
        self.slack_client.rtm_connect() # connect to the real-time messaging system

        slack_test = json.loads(self.slack_client.api_call('auth.test'))
        self.user = User(slack_test['user_id'], slack_test['user'])
        logging.info("I am @%s, uid %s", self.user.name, self.user.uid)

    def load_plugins(self, plugins, plugindir):
        if plugins is not None:
            for plugin in plugins:
                logging.debug('loading plugin %s from %s', plugin, plugindir)

                fp, path, desc = imp.find_module(plugin, [plugindir])

                try:
                    imp.load_module(plugin, fp, path, desc)
                finally:
                    if fp:
                        fp.close()

    def brew(self):
        """Run the bot.
        Starts an infinite processing loop.
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
                        message = Message(User(msg['user'], self.slack_client.server.users.find(msg['user']).name),
                                self.slack_client.server.channels.find(msg['channel']),
                                msg['text'])
                        for listener in self.listeners:
                            listener.call(message)

            # TODO: take loaded list of plugin callback regexes and check them, then call the callbacks
            time.sleep(.1)

    def add_listener(self, ltype, regex, function, **options):
        if ltype == ListenerType.heard:
            self.listeners.append(Listener(self, regex, function))
        elif ltype == ListenerType.heard_with_name:
            regex = "^(?:\<\@U0A9396LC\>|{})\s*:?\s*".format(self.user.name) + regex
            self.listeners.append(Listener(self, regex, function))
        logging.debug("Added listener of type %s with regex %s calling %s", ltype, regex, function.__name__)

    # THESE ARE DECORATORS !!!
    def hear(self, regex, **options):
        def decorator(f):
            self.add_listener(ListenerType.heard, regex, f, **options)
            return f
        return decorator

    def respond(self, regex, **options):
        def decorator(f):
            self.add_listener(ListenerType.heard_with_name, regex, f, **options)
            return f
        return decorator
    # END DECORATORS !!!

    def send(self, message, channel):
        logging.debug("Send message %s to #%s", message, channel)
        logging.debug("message type: %s ; channel type %s", type(message), type(channel))
        self.slack_client.server.channels.find(channel).send_message(message)
