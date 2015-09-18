import logging
import re

from enum import Enum
from response import Response


class ListenerType(Enum):
    heard = 1
    heard_with_name = 2


class Listener(object):
    def __init__(self, robot, regex, callback, options):
        self.robot = robot
        self.regex = re.compile(regex)
        self.callback = callback
        self.options = options

    def __repr__(self):
        return "<Listener regex:{}, callback:{}>".format(self.regex.pattern, self.callback.__name__)

    def call(self, message):
        matches = message.match(self.regex)
        if matches:
            logging.debug("%s matches %s", message.text, self.regex.pattern)
            self.callback(Response(self.robot, message, matches))
