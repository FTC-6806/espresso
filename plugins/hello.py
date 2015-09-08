# Be friendly

import random
from espresso.main import robot

@robot.respond('(?i)(hi)|(hello)|(howdy)|(hallo)')
def hello(res):
    res.reply(res.msg.user, "Hi there!")
