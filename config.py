from pathlib import Path


# project settings
ROOT_DIR = str(Path(__file__).parent).replace('\\', '/')

DEBUG = True

# bot settings
BOT_TOKEN="5653382112:AAHMkPkewFI5491iqoB0FEdbwgyg1UJu8fk"
BOT_OWNER=501616979

CHANNEL_URL = "https://t.me/+qX5IQnt-Z4NhMzRi"
CHANNEL_ID = "-1001459767409"


# database settings
DATABASE_NAME = 'bot.sqlite3'
DATABASE_URL = f'sqlite:///{ROOT_DIR}/' + DATABASE_NAME + '?check_same_thread=False'


