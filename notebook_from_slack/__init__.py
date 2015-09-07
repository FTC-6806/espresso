"""
    Notebook From Slack
    ~~~~~~~~~~~~~~~~~~~
    An application to curate Slack posts into
    Engineer's Notebook entry templates.
    :copyright: (c) 2015 by Liam Marshall
    :license: BSD, see LICENSE for more details.
"""

from flask import Flask
app = Flask(__name__)

import notebook_from_slack.api