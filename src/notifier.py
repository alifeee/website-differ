from pushbullet import Pushbullet
from dotenv import load_dotenv
import os

load_dotenv()

PUSHBULLET_ACCESS_TOKEN = os.getenv("PUSHBULLET_ACCESS_TOKEN")
pb = Pushbullet(PUSHBULLET_ACCESS_TOKEN)


def notify(title, message):
    push = pb.push_note(title, message)


def notify_file(filename, file_content):
    file_data = pb.upload_file(file_content, filename)
    push = pb.push_file(**file_data)


if __name__ == "__main__":
    notify("notify()", "This is a test notification")
    notify_file("test.txt", "This is a test file")
