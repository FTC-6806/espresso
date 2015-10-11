from nose.tools import *
import mock

@mock.patch("espresso.bot.Espresso")
def test_matching_heard(Espresso):
	from espresso.listener import Listener
	from espresso.message import Message
	from espresso.user import User

	FAKE_USER = User("fake_id", "fake_name")
	FAKE_MESSAGE = Message(FAKE_USER, "fake-channel", "THIS should MATCH")

	robot = Espresso()
	mock_callback = mock.MagicMock()

	listener = Listener(robot, r"(THIS) (\w*) (MATCH)", mock_callback)
	listener.call(FAKE_MESSAGE)

	assert mock_callback.called
