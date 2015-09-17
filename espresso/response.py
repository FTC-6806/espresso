import logging


class Response(object):
    """The object sent back to the callback
    Contains methods for calling senders and responders on Espresso
    """
    def __init__(self, robot, msg, match):
        self.robot = robot
        self.msg = msg
        self.match = match

    def send(self, message, channel=None):
        channel = self.msg.channel.name or channel
        self.robot.send(message, channel)

    def reply(self, user, message, channel=None):
        channel = self.msg.channel.name or channel
        logging.debug("message %s on channel #%s to user @%s", message, channel, user.name)
        self.robot.send("@{}: {}".format(user.name, message), channel)
