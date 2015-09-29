import re


class Message(object):
    """Holds a message and its data."""

    def __init__(self, user, channel, text):
        self.user = user
        self.text = text
        self.channel = channel

    def __repr__(self):
        """A nice pretty-printing in the REPL"""

        return "<Message user:{} channel:{} text:{}>".format(self.user, self.channel, self.text)

    def match(self, regex):
        """Does the message match the regex?

        Uses re.search.
        Takes compiled regex.
        """

        return re.search(regex, self.text)
