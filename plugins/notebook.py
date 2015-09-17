# the notebook plugin
# handles notebook creation

import dateutil.parser
import logging

import json
import re

from docx import Document
from espresso.main import robot
from tinydb import where

ANNOUNCEMENT_REGEX = r'(?is)Announcement for (?P<date>\d+/\d+/\d+): (?P<announcement>.*)'


@robot.hear(ANNOUNCEMENT_REGEX)
def got_announcement(res):
    date = dateutil.parser.parse(res.match.group('date'))
    announcement = res.match.group('announcement')
    user = res.msg.user.name

    logging.debug("Got Announcement for date %s: %s", date, announcement)
    res.robot.brain.db.insert({"plugin": "notebook", "type": "announcement",
        "date": date.isoformat(), "announcement": announcement,
        "user": user, "channel": res.msg.channel.name})

@robot.respond(r'(?i)backfill announcements for (?P<date>\d+/\d+/\d+)')
def backfill_announcements(res):
    target_date = dateutil.parser.parse(res.match.group('date'))

    channel_history = json.loads(res.robot.slack_client.api_call('channels.history',
        channel=res.robot.slack_client.server.channels.find("announcements").id,
        inclusive=1))
    channel_message_type_events = channel_history['messages']
    channel_messages = filter(lambda m: ((m.get('type') == 'message') and ('subtype' not in m)), channel_message_type_events)

    for m in channel_messages:
        match = re.search(ANNOUNCEMENT_REGEX, m['text'])
        if match:
            date = dateutil.parser.parse(match.group('date'))
            announcement = match.group('announcement')
            user = res.robot.slack_client.server.users.find(m['user']).name
            if date == target_date:
                logging.debug("Got Announcement for date %s by user %s: %s",
                              date, user, announcement)
                res.robot.brain.db.insert({"plugin": "notebook", "type": "announcement",
                    "date": date.isoformat(), "announcement": announcement,
                    "user": user, "channel": 'announcements'})



@robot.respond('(?i)make a (new )?notebook (entry|template) for (?P<date>\d+/\d+/\d+)')
def make_entry(res):
    date = dateutil.parser.parse(res.match.group('date'))
    logging.debug("date: %s", date)
    logging.debug("db dump: %s", res.robot.brain.db.all())
    announcements = res.robot.brain.db.search((where('plugin') == 'notebook')
        & (where('type') == 'announcement')
        & (where('date') == date.isoformat())
        )

    logging.debug("announcements are %s", announcements)

    if announcements != []:
        document = Document()
        document.add_page_break()
        document.add_heading('{date}, the BEC'.format(date=date.strftime('%m/%d/%Y')), level=1)
        document.add_paragraph('Present team members: <enter them here>')
        document.add_heading('Announcements:', level=2)

        users = []
        for announcement in announcements:
            if announcement['user'] not in users:
                users.append(announcement['user'])

        logging.debug("users are %s", users)

        for user in sorted(users):
            real_name = res.robot.slack_client.server.users.find(user).real_name
            logging.debug("announcing user %s is %s", user, real_name)
            document.add_heading("{}:".format(real_name), level=3)
            for announcement in announcements:
                if announcement['user'] == user:
                    document.add_paragraph("{}".format(announcement['announcement']), style='ListBullet')

        document.save('test.docx')
