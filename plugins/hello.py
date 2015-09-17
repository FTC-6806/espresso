# Be friendly

import random

from espresso.main import robot

HELLOS = [
    "Well hello there!"
    "Hello!",
    "Hi there!",
    "Hallo!"
]

@robot.respond(r'(?i)(hi)|(hello)|(howdy)|(hallo)')
def hello(res):
    res.reply(res.msg.user, random.choice(HELLOS))
