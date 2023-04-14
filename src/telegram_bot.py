import asyncio
import telegram
from dotenv import load_dotenv
import os

load_dotenv()
try:
    api_key = os.environ['TELEGRAM_BOT_ACCESS_TOKEN']
except KeyError:
    raise ValueError(
        "TELEGRAM_BOT_ACCESS_TOKEN not found in environment variables")


async def main():
    bot = telegram.Bot(api_key)
    async with bot:
        print(await bot.get_me())

if __name__ == '__main__':
    asyncio.run(main())
