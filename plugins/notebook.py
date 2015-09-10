# the notebook plugin
# handles notebook creation

import dateutil.parser
import logging

from docx import Document
from espresso.main import robot
from tinydb import where


@robot.hear('(?i)Announcement for (?P<date>[0-9]?[0-9]\/[0-9]?[0-9]\/[0-9][0-9]): (?P<announcement>.*)')
def got_announcement(res):
    date = dateutil.parser.parse(res.match.group('date'))
    announcement = res.match.group('announcement')
    user = res.msg.user.name

    logging.debug("Got Announcement for date %s: %s", date, announcement)
    res.robot.brain.db.insert({"plugin": "notebook", "type": "announcement",
        "date": date.isoformat(), "announcement": announcement,
        "user": user, "channel": res.msg.channel.name})

