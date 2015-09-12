# the notebook plugin
# handles notebook creation

import dateutil.parser
import logging

from docx import Document
from espresso.main import robot
from tinydb import where


@robot.hear('(?i)Announcement for (?P<date>\d+/\d+/\d+): (?P<announcement>.*)')
def got_announcement(res):
    date = dateutil.parser.parse(res.match.group('date'))
    announcement = res.match.group('announcement')
    user = res.msg.user.name

    logging.debug("Got Announcement for date %s: %s", date, announcement)
    res.robot.brain.db.insert({"plugin": "notebook", "type": "announcement",
        "date": date.isoformat(), "announcement": announcement,
        "user": user, "channel": res.msg.channel.name})

@robot.respond('(?i)make a (new )?notebook (entry|template) for (?P<date>\d+/\d+/\d+)')
def make_entry(res):
    date = dateutil.parser.parse(res.match.group('date'))
    announcements = res.robot.brain.db.search(
        (where('plugin') == 'notebook') &
        (where('type') == 'announcement') & 
        (where('date') == date.isoformat())
        )

    res.reply(res.msg.user, announcements)

    # document = Document()
