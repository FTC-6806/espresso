from nose.tools import *

def test_message_storage_consistency():
	from espresso.user import User
	from espresso.message import Message

	FAKE_USER = User("f00f", "jimmy depreaux")
	FAKE_MESSAGE_TEXT = "watch out for traffic!"
	FAKE_CHANNEL = "safety-warnings"

	a_message = Message(FAKE_USER,
		FAKE_CHANNEL,
		FAKE_MESSAGE_TEXT)

	assert a_message.user is FAKE_USER
	assert a_message.text == FAKE_MESSAGE_TEXT
	assert a_message.channel == FAKE_CHANNEL

def test_message_matching():
	from espresso.user import User
	from espresso.message import Message

	FAKE_USER = User("f00f", "jimmy depreaux")
	FAKE_MESSAGE_TEXT = "watch out for traffic!"
	FAKE_CHANNEL = "safety-warnings"

	a_message = Message(FAKE_USER,
		FAKE_CHANNEL,
		FAKE_MESSAGE_TEXT)

	assert a_message.match("asdfasdf") is None
	assert a_message.match("watch out") is not None