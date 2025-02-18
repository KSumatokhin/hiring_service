import os
from dotenv import load_dotenv


load_dotenv('.env')
TOKEN: str = os.getenv('BOT_TOKEN')