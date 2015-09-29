from .listener import ListenerType


class PluginAPI(object):
    """Holds the decorator-based plugin PluginAPI.

    It gets mixed in to the main Espresso class, which is what plugins call the API off of.
    Having a seperate class is _not_ necessary, but it's nicer to hack on.
    """

    def hear(self, regex, **options):
        """Adds a "heard" type listener regex."""

        def decorator(f):
            self.add_listener(ListenerType.heard, regex, f, options)
            return f
        return decorator

    def respond(self, regex, **options):
        """Adds a "heard_with_name" type listener regex."""

        def decorator(f):
            self.add_listener(ListenerType.heard_with_name, regex, f, options)
            return f
        return decorator
