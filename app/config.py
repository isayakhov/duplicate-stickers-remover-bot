import logging
import os

APP_VERSION = os.getenv("APP_VERSION", "0.1.0")

STICKERS_ROOT_DIRECTORY = os.getenv("STICKERS_ROOT_DIRECTORY", os.path.dirname(__file__))

AVERAGE_HASH_THRESHOLD_VALUE = int(os.getenv("AVERAGE_HASH_THRESHOLD_VALUE", "8"))

TELEGRAM_BOT_NAME = os.getenv("TELEGRAM_BOT_NAME", "FILL_ME")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "FILL_ME")

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
