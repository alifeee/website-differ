# Web differ

This project is a frontend for keeping track of static websites to see if they change.

<http://server.alifeee.co.uk:5616>

![Screenshot of frontend](images/frontend_screenshot.png)

## Usage

### Install dependencies

```bash
pip install -r requirements.txt
playwright install
```

### Add websites to track

Use the web client.

### Run

```bash
mkdir snapshots
echo "id,url,css_selector\n" > sites.csv
py ./server.py
```

Set up cron

```bash
crontab -e
```

```bash
# Run every day
0 12 * * * cd /path/to/web-differ && /usr/bin/python3 /path/to/web-differ/snapshotall.py >> /path/to/web-differ/cron.log 2>&1
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
