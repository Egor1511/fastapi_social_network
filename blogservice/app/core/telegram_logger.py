import logging
import os

import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


class TelegramHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        message = f"Critical Error:\n{log_entry}"
        send_telegram_message(message)


def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        logging.error("Failed to send message to Telegram: %s", e)


def setup_telegram_logging():
    telegram_handler = TelegramHandler()
    telegram_handler.setLevel(logging.CRITICAL)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    telegram_handler.setFormatter(formatter)
    logging.getLogger().addHandler(telegram_handler)
