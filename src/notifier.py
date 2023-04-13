from pushbullet import Pushbullet
from dotenv import load_dotenv
import os

load_dotenv()

try:
    PUSHBULLET_ACCESS_TOKEN = os.environ["PUSHBULLET_ACCESS_TOKEN"]
except KeyError as e:
    raise e from EnvironmentError(
        "PUSHBULLET_ACCESS_TOKEN not set. Please set it in .env. See README.md for more info.")
try:
    pb = Pushbullet(PUSHBULLET_ACCESS_TOKEN)
except Exception as e:
    raise e from Exception(
        "Error while connecting to Pushbullet. Please check your PUSHBULLET_ACCESS_TOKEN. See README.md for more info.")


def notify(title: str, message: str):
    prepend = "Website Monitor: "
    push = pb.push_note(prepend + title, message)


def notify_file(filename: str, file_content: str):
    file_data = pb.upload_file(file_content, filename)
    push = pb.push_file(**file_data)


if __name__ == "__main__":
    notify("notify()", "This is a test notification")
    notify_file("test.txt", "This is a test file")
