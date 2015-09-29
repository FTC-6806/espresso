from tinydb import TinyDB


# TODO: Implement an actual API around the DB for encapsulation of plugin data and easy storage and retrieval
class Brain(object):
    """Holds robot state."""

    def __init__(self, db_location):
        """Initalize the brain.

        Creates a new TinyDB instance working on the DB at db_location.

        Args:
            db_location: a string with the path to a TinyDB
        """

        self.db = TinyDB(db_location)
