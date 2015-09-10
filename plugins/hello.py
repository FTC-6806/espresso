# Be friendly

import random

from espresso.main import robot

hellos = [
    "Well hello there!"
    "Hello!",
    "Hi there!",
    "Hallo!"
]

@robot.respond('(?i)(hi)|(hello)|(howdy)|(hallo)')
def hello(res):
    res.reply(res.msg.user, random.choice(hellos))
