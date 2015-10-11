from nose.tools import *

def test_user_storage_consistency():
	from espresso.user import User

	FAKE_ID = "a_fake_id"
	FAKE_NAME = "a_fake_name"

	a_user = User(FAKE_ID, FAKE_NAME)

	assert a_user.uid == FAKE_ID
	assert a_user.name == FAKE_NAME

def test_user_default_name():
	from espresso.user import User

	FAKE_ID = "a_fake_id"

	a_user = User(FAKE_ID)

	assert a_user.name == "?"