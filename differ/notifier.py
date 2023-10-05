"""Different notifier implementations."""
import os
from datetime import datetime
from dotenv import load_dotenv
from pushbullet import Pushbullet

load_dotenv()


class NotifierInterface:
    """Notifier interface."""

    def __init__(self, level: int = 0):
        """Initialize notifier."""
        self.level = level

    def notify(self, message, level=0):
        """Notify the user about the message."""
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")
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


class PushbulletNotifier(NotifierInterface):
    """Notifier using Pushbullet's API"""

    def __init__(self, level: int = 0):
        """Initialize notifier."""
        super().__init__(level)
        try:
            token = os.environ["PUSHBULLET_API_TOKEN"]
        except KeyError as err:
            raise err from EnvironmentError(
                """PUSHBULLET_API_TOKEN not set.
                Please set it in .env. See README.md for more info."""
            )

        self.pushbullet = Pushbullet(token)

    def _notify(self, message):
        """Notify the user about the message."""
        self.pushbullet.push_note(
            "Differ",
            message,
        )


if __name__ == "__main__":
    notifier = PushbulletNotifier(0)
    notifier.notify("hello")
