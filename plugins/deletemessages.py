# Delete the last n messages sent by the bot
# Very useful for cleaning up after testing
# Manually interacts with Slack's API through res.robot.slack_client.api_call

from espresso.main import robot
import json
import logging
import itertools

@robot.respond("(?i)delete your last (?P<howmany>[0-9]*) messages")
def delete_n_messages(res):
    howmany = int(res.match.group('howmany'))
    channel_history = json.loads(res.robot.slack_client.api_call('channels.history',
        channel=res.msg.channel.id,
        inclusive=1))
    channel_messages = channel_history['messages']

    my_messages = filter(lambda m: ((m.get('type') == 'message') and ('subtype' not in m) and (m['user'] == robot.user.uid)), channel_messages)

    for message in itertools.islice(my_messages, howmany):
        logging.debug("deleting message with content %s", message['text'])
        res.robot.slack_client.api_call("chat.delete",
            ts=message['ts'],
            channel=res.msg.channel.id)

    logging.debug("deleted my last %i messages in the channel %s",
        howmany, res.msg.channel.name)
