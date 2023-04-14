import asyncio
import telegram
from dotenv import load_dotenv
import os

load_dotenv()
try:
    api_key = os.environ['TELEGRAM_BOT_ACCESS_TOKEN']
    chat_id = os.environ['TELEGRAM_PERSONAL_CHAT_ID']
except KeyError:
    raise ValueError(
        "TELEGRAM_BOT_ACCESS_TOKEN not found in environment variables")


async def main():
    bot = telegram.Bot(api_key)
    async with bot:
        await bot.send_message(chat_id, "Hello World")

if __name__ == '__main__':
    asyncio.run(main())
