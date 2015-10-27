from espresso.main import robot

@robot.respond(r"(?i)pass the butter")
def pass_the_butter(res):
    res.reply(res.msg.user, "What is my purpose in life?")

@robot.respond(r"(?i)you pass butter")
def you_pass_butter(res):
    res.send("Oh my god.")
