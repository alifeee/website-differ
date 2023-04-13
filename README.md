# Web differ

This project takes a snapshot of a website and compares it to a previous snapshot. If the website has changed, it sends a notification.

It does not continually run, but is intended to be run as a cron job.

It does not use a headless browser, but instead uses the requests library to get the HTML of the page. This means that it is not as accurate as a headless browser, and if a website uses javascript to render some of a page, it will not be able to detect this.

![Example notification on pushbullet, showing website URL and the new HTML file](images/pushbullet_ping.png)

## Usage

The website URLs are stored in `urls.txt`, which is not tracked by git.

### `urls.txt`

```txt
https://www.example.com
https://www.example.org
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run

```bash
python src/main.py
```

## Development

### Requirements

| Name | Version |
| ---- | ------- |
| Python | 3.8.2 |
| pip | 20.0.2 |

### Main modules used

| Name | Version |
| ---- | ------- |
| [pushbullet.py](https://github.com/richard-better/pushbullet.py) | 0.12.0 |
| [requests](https://github.com/psf/requests) | 2.28.0 |
| [sqlite3](https://docs.python.org/3/library/sqlite3.html) | base dependency [(pi note)](./SQLITE3_on_PI.md) |

### Set up virtual environment

```bash
py -m venv env
```

### Save dependencies

```bash
pip freeze > requirements.txt
```

## Notifications

Notifications are sent via pushbullet. To set up pushbullet via python, you need to set up an access token, found in the [user settings](https://www.pushbullet.com/#settings/account).
These are stored in a `.env` file.

```.env
PUSHBULLET_ACCESS_TOKEN=...
```

See more information on <https://pypi.org/project/pushbullet.py/0.9.1/>.

## Database

SQLite is used for the database, which is stored in a local file `websites.db`. This is not tracked by git.

### Create database

```bash
sqlite3 websites.db < schema.sql
```

### Print database

```bash
sqlite3 websites.db
> .tables
> .schema
> .headers on
> SELECT * FROM queries;
> ...
```
