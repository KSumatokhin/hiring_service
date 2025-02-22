
import logging
import os

from dotenv import load_dotenv
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


load_dotenv('.env')
BOT_TOKEN: str = os.getenv('BOT_TOKEN')
IMAGE_FILE_PATH = '..\\..\\media\\X1ljFRq5wC0.jpg'
# IMAGE_FILE_PATH = 'G:\\Project-Git\\hiring_service\\media\\X1ljFRq5wC0.jpg'


async def photo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_photo(photo=open(IMAGE_FILE_PATH, 'rb'))



def main() -> None:

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, photo_command))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()