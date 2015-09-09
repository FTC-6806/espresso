# the question. you know the one

from espresso.main import robot

@robot.respond("(?i)what is the answer to the (ultimate )?question of life, the universe, and everything")
def theanswer(res):
    res.reply(res.msg.user, "There really is one, though I don't think you're going to like it.")
