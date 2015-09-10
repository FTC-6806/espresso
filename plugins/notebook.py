# the notebook plugin
# handles notebook creation

import dateutil.parser
from espresso.main import robot
from docx import Document


@robot.hear('(?i)Announcement for (?P<date>[0-9]?[0-9]\/[0-9]?[0-9]\/[0-9][0-9]): (?P<announcement>.*)')
def got_announcement(res):
    date = dateutil.parser.parse(res.match.group('date'))
    announcement = res.match.group('announcement')
    user = res.msg.user.name

    res.reply(res.msg.user, "Got Announcement for date {}: {}".format(date, announcement))
    res.robot.brain.db.insert({"plugin": "notebook", "type": "announcement",
        "date": date.isoformat(), "announcement": announcement,
        "user": user, "channel": res.msg.channel.name})

