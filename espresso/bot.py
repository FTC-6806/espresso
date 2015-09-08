import imp
import logging
import os
import re
import time

from slackclient import SlackClient

from repl import EspressoConsole

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

    def connect(self):
        """Helper method to connect to Slack.
        Creates a new SlackClient with ``self.api_token``.
        """

        self.slack_client = SlackClient(self.api_token)
        self.slack_client.rtm_connect() # connect to the real-time messaging system

    def brew(self):
        """Run the bot.
        Starts an infinite processing loop.
        """

        logging.info("starting the bot")
        self.connect()

        if self.config['debug_console']:
            espresso_console = EspressoConsole(locals())
            espresso_console.interact()

        while True:
            for reply in self.slack_client.rtm_read():
                print(reply)
            # TODO: take loaded list of plugin callback regexes and check them, then call the callbacks
            time.sleep(.1)

    def add_listener(ltype, regex, function, **options):
        logging.debug("Add listener of type %s with regex %s calling %s", ltype.__name__, regex, function.__name__)


    def hear(self, regex, **options):
        def decorator(f):
            self.add_listener(HEARD, regex, f, **options)
            return f
        return decorator

    def respond(self, regex, **options):
        def decorator(f):
            self.add_listener(HEARD_WITH_NAME, regex, f, **options)
            return f
        return decorator
