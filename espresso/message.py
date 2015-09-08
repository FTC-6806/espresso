import re

class Message(object):
    def __init__(self, user, channel, text):
        self.user = user
        self.text = text
        self.channel = channel

    def __repr__(self):
        return "{} on {}: {}".format(self.user, self.channel, self.text)

    def match(self, regex):
        """Does the message match the regex?
        Uses re.search.
        Takes compiled regex.
        """
        return re.search(regex, self.text)
