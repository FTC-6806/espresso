# the notebook plugin
# handles notebook creation

import dateutil.parser
import logging

from docx import Document
from espresso.main import robot
from tinydb import where


@robot.hear('(?is)Announcement for (?P<date>\d+/\d+/\d+): (?P<announcement>.*)')
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
            document.add_paragraph("{}:".format(real_name))
            for announcement in  filter(lambda a: a['user'] == user, announcements):
                document.add_paragraph("{}".format(announcement['announcement']), style='ListBullet')

        document.save('test.docx')
