# the notebook plugin
# handles notebook creation

from espresso.main import robot

@robot.hear('(?i)Announcement for (?P<date>[0-9][0-9]\/[0-9][0-9]\/[0-9][0-9]): (?P<announcement>.*)')
def got_announcement(res):
    date = res.match.group('date')
    announcement = res.match.group('announcement')

    res.reply(res.msg.user, "Got Announcement for date {}: {}".format(date, announcement))
