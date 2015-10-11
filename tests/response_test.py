from nose.tools import *
import mock

@mock.patch("espresso.bot.Espresso")
def test_response_send_msg(Espresso):
	robot = Espresso()