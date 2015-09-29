class User(object):
    """Simple wrapper for storing user data"""

    def __init__(self, uid, name="?"):
        self.uid = uid
        self.name = name
