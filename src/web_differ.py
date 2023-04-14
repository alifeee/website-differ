import requests
from .notifier import notify, notify_file
from .database import Database


def poll_and_notify():
    db = Database("websites.db")

    try:
        with open("urls.txt", "r") as f:
            urls = f.read().splitlines()
    except Exception as e:
        raise e from Exception("Error reading urls.txt. Does it exist?")

    for url in urls:
        last_date, last_content = db.getLatestSnapshot(url)

        r = requests.get(url)
        try:
            website_content = r.text
            db.recordSnapshot(url, website_content)
        except Exception as e:
            notify(f"Error for {url}: {e}")
            continue

        if last_content is None and last_date is None:
            notify("New website added", url)
            print(f"New website: {url}")
        elif last_content != website_content:
            notify("Website changed", url)
            notify_file("new_site.html", website_content)
            print(f"Change for {url}")
        elif last_content == website_content:
            print(f"No change for {url}")
        else:
            notify(f"Database error for {url}")
            raise Exception("Database error")
