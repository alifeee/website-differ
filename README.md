# Web differ

This project takes a snapshot of a website and compares it to a previous snapshot. If the website has changed, it sends a notification. See the process outlined in [process.tldr](./process.tldr).

It does not continually run, but is intended to be run as a cron job.

It does not use a headless browser, but instead uses the requests library to get the HTML of the page. This means that it is not as accurate as a headless browser, and if a website uses javascript to render some of a page, it will not be able to detect this.

![Example notification on pushbullet, showing website URL and the new HTML file](images/pushbullet_ping.png)

## Usage

### Install dependencies

```bash
pip install -r requirements.txt
```

### Add websites to track

```bash
py -m src.database_cli websites add <url>
...
```

### Run

```bash
python ./main.py
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
| [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) | 20.2 |
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

Notifications are sent via [Telegram](https://telegram.org/). Secrets are used via environment variables, or a `.env` file, which is not tracked by git.

```bash
touch .env
```

```.env
TELEGRAM_BOT_ACCESS_TOKEN=...
TELEGRAM_PERSONAL_CHAT_ID=...
```

### How to get bot access token

See [help page](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API), but in essence, talk to the [BotFather](https://t.me/botfather).

### How to get personal chat ID

See [help page](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API), but in essence, send the bot a message and then use the `getUpdates` method.

```python
import asyncio
import telegram

async def main():
    bot = telegram.Bot("TOKEN")
    async with bot:
        print((await bot.get_updates())[0])

if __name__ == '__main__':
    asyncio.run(main())
```

## Database

SQLite is used for the database, which is stored in a local file `websites.db`. This is not tracked by git.

### Create database

```bash
sqlite3 websites.db < schema.sql
```

### View database in terminal

```bash
sqlite3 websites.db
> .tables
> .schema
> .headers on
> SELECT * FROM queries;
> ...
> SELECT * FROM websites;
> ...
> .quit
```
