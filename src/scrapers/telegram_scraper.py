import os
import sys
sys.path.append('..')
import json
from datetime import datetime
import logging
from telethon.tl.functions.messages import GetHistoryRequest
from src.config.settings import client
from src.utils.logger import ensure_dir

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

async def scrape_text_messages(channel_url, limit=100):
    entity = await client.get_entity(channel_url)
    today = datetime.utcnow().strftime('%Y-%m-%d')
    folder = os.path.join(PROJECT_ROOT, "data", "raw", "telegram_messages", today, entity.username)
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

    enriched_messages = []

    for msg in history.messages:
        msg_dict = msg.to_dict()

        # Extract basic media metadata if media exists
        if msg.media:
            msg_dict['media_info'] = {
                'caption': getattr(msg.media, 'caption', None),
                'media_type': msg.media.__class__.__name__,
                'mime_type': getattr(msg.media, 'mime_type', None),
                'size': getattr(msg.media, 'size', None),
                'file_reference': str(getattr(msg.media, 'file_reference', b'').hex()),
            }

        enriched_messages.append(msg_dict)

    file_path = os.path.join(folder, 'all_messages_with_metadata.json')
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(enriched_messages, f, ensure_ascii=False, indent=2, default=str)

    logging.info(f"Scraped {len(enriched_messages)} messages (including media metadata) from {channel_url}")
    return history.messages, entity.username, today
