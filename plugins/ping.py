# basic "is it alive" tests and simple admin
import sys
import datetime

from espresso.main import robot

@robot.respond("(?i)PING")
def ping(res):
    res.send("PONG")

@robot.respond("(?i)ECHO (?P<echotext>.*)")
def echo(res):
    res.send(res.match.group('echotext'))

@robot.respond("(?i)TIME\?*")
def time(res):
    res.send("Server time is {}".format(datetime.datetime.now().ctime()))

@robot.respond("(?i)DIE")
def die(res):
    res.send("Goodbye, cruel world.")
