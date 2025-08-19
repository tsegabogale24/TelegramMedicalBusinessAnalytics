# models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Message(Base):
    __tablename__ = "fct_messages"
    __table_args__ = {'schema': 'raw_analytics'}

    message_id = Column(Integer, primary_key=True, index=True)
    channel_name = Column(String, index=True)
    message_date = Column(DateTime)
    message_length = Column(Integer)
    has_image = Column(Boolean)
    message_text = Column(Text)
    product_name = Column(String, nullable=True)


class ImageDetection(Base):
    __tablename__ = "fct_image_detections"
    __table_args__ = {'schema': 'raw'}

    detection_id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer)
    detected_object_class = Column(String)
    confidence_score = Column(Float)
    image_url = Column(String, nullable=True)
