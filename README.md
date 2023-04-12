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

### Set up local mail server

```bash
python -m smtpd -n DebuggingServer localhost:1025
```

### Secrets

These are stored in a `.env` file.

```.env
MAIL_PASSWORD=...
MAIL_SERVER=...
```
