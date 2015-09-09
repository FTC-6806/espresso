from tinydb import TinyDB, where

class Brain(object):
    """The robot's brain.
    Uses TinyDB to store stuff into a simple, flat-json-file on-disk db.
    If you want to Espresso on Heroku or any other diskless PaaS,
    you can wire in MongoDB or something instead.
    """

    def __init__(self, db_location):
        self.db = TinyDB(db_location)
