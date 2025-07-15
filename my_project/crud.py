# crud.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import Message, Channel, ImageDetection, Date
from typing import List

def get_channel_activity(db: Session, channel_name: str):
    return (
        db.query(
            func.date_trunc('day', Date.date).label("date"),
            func.count()
        )
        .select_from(Message)
        .join(Channel, Channel.channel_id == Message.channel_id)
        .join(Date, Date.date_id == Message.date_id)
        .filter(Channel.channel_name == channel_name)
        .group_by(func.date_trunc('day', Date.date))
        .order_by(func.date_trunc('day', Date.date))
        .all()
    )


def get_top_products(db: Session, limit: int = 10) -> List[str]:
    return (
        db.query(Message.product_name, func.count().label("count"))
        .filter(Message.product_name.isnot(None))
        .group_by(Message.product_name)
        .order_by(func.count().desc())
        .limit(limit)
        .all()
    )

def search_messages(db: Session, query: str):
    return (
        db.query(Message)
        .filter(Message.message_text.ilike(f"%{query}%"))
        .limit(100)
        .all()
    )
