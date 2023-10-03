"""Different notifier implementations."""


class NotifierInterface:
    """Notifier interface."""

    def __init__(self, level: int = 0):
        """Initialize notifier."""
        self.level = level

    def notify(self, message, level=0):
        """Notify the user about the message."""
        if level >= self.level:
            self._notify(message)

    def _notify(self, message):
        """Notify the user about the message."""
        raise NotImplementedError


class PrintNotifier(NotifierInterface):
    """Print notifier."""

    def _notify(self, message):
        """Print the message."""
        print(message)
