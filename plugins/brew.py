# Make me coffee!
# maybe someday we'll actually make this order coffee using a phone-connection service :D

from espresso.main import robot

@robot.respond(r'(?i)make (me )?(a )?coffee')
def make_coffee(res):
    res.reply(res.msg.user, "http://dreamatico.com/data_images/coffee/coffee-3.jpg")
