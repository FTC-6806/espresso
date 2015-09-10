from tinydb import TinyDB
from tinydb import where

class Brain(object):
    def __init__(self, db_location):
        self.db = TinyDB(db_location)
