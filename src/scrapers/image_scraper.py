import os
import sys
import logging
from datetime import datetime
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import MessageMediaPhoto
from src.config.settings import client
from src.utils.logger import ensure_dir

sys.path.append('..')
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

async def scrape_images_from_channel(channel_url, limit=100):
    await client.connect()
    if not await client.is_user_authorized():
        logging.error("Client is not authorized. Please log in.")
        return

    entity = await client.get_entity(channel_url)
    today = datetime.utcnow().strftime('%Y-%m-%d')

    folder = os.path.join(PROJECT_ROOT, "data", "raw", "telegram_images", today, entity.username)
    ensure_dir(folder)

    history = await client(GetHistoryRequest(
        peer=entity,
        limit=limit,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))

    image_count = 0
    for msg in history.messages:
        if msg.media and isinstance(msg.media, MessageMediaPhoto):
            await client.download_media(msg, folder)
            image_count += 1

    logging.info(f"Downloaded {image_count} images from {channel_url}")
    await client.disconnect()
