# Web differ

This project takes a snapshot of a website and compares it to a previous snapshot. If the website has changed, it sends a notification.

It does not continually run, but is intended to be run as a cron job.

## Usage

### Install dependencies

```bash
pip install -r requirements.txt
playwright install
```

### Add websites to track

```bash
# todo
```

### Run

```bash
mkdir snapshots
echo "id,url,css_selector\n" > sites.csv
py ./server.py
```

## Development

### Set up virtual environment

```bash
py -m venv env
```

### Save dependencies

```bash
pip freeze > requirements.txt
```

## Notifications

Notifications are sent via Pushbullet. To set up Pushbullet via python, you need to set up an access token, found in the [user settings](https://www.pushbullet.com/#settings/account).
These are stored in a `.env` file.

```.env
PUSHBULLET_ACCESS_TOKEN=...
```

See more information on <https://pypi.org/project/pushbullet.py/0.9.1/>.
