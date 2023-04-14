import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from dotenv import load_dotenv
import os

load_dotenv()
try:
    api_key = os.environ['TELEGRAM_BOT_ACCESS_TOKEN']
    chat_id = os.environ['TELEGRAM_PERSONAL_CHAT_ID']
except KeyError:
    raise ValueError(
        "Please set the TELEGRAM_BOT_ACCESS_TOKEN and TELEGRAM_PERSONAL_CHAT_ID environment variables."
    )

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I am a bot, please talk to me!")

if __name__ == '__main__':
    application = ApplicationBuilder().token(api_key).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()
