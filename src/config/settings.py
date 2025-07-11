import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient

load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

client = TelegramClient("Ethio-scraper", api_id, api_hash)


print("Client is logged in.")
