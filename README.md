# Web differ

This project takes a snapshot of a website and compares it to a previous snapshot.

## Development

### Set up the environment

```bash
py -m venv env
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Save dependencies

```bash
pip freeze > requirements.txt
```

### Secrets

These are stored in a `.env` file.

```.env
PUSHBULLET_ACCESS_TOKEN=...
```

The pushbullet access token can be found in the [Pushbullet settings](https://www.pushbullet.com/#settings/account). See more information on <https://pypi.org/project/pushbullet.py/0.9.1/>.


```bash
python -m smtpd -n DebuggingServer localhost:1025
```

### Secrets

These are stored in a `.env` file.

```.env
MAIL_PASSWORD=...
MAIL_SERVER=...
```
