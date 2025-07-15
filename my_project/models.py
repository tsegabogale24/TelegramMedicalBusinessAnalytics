# models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Channel(Base):
    __tablename__ = "dim_channels"
    __table_args__ = {'schema': 'raw_analytics'}

    channel_id = Column(Integer, primary_key=True, index=True)
    channel_name = Column(String, unique=True, nullable=False)
    channel_type = Column(String, nullable=True)  # Optional, if available

    # Relationships (optional, not required unless using ORM joins)
    messages = relationship("Message", back_populates="channel")


class Date(Base):
    __tablename__ = "dim_dates"
    __table_args__ = {'schema': 'raw_analytics'}

    date_id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    weekday = Column(String)
    week = Column(Integer)

    messages = relationship("Message", back_populates="date")


class Message(Base):
    __tablename__ = "fct_messages"
    __table_args__ = {'schema': 'raw_analytics'}

    message_id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("dim_channels.channel_id"))
    date_id = Column(Integer, ForeignKey("dim_dates.date_id"))
    message_text = Column(Text)
    message_length = Column(Integer)
    has_image = Column(Boolean)

    # Optional: if you did entity extraction to get product mentions
    product_name = Column(String, nullable=True)

    # Relationships
    channel = relationship("Channel", back_populates="messages")
    date = relationship("Date", back_populates="messages")
    image_detections = relationship("ImageDetection", back_populates="message")


class ImageDetection(Base):
    __tablename__ = "fct_image_detections"
    __table_args__ = {'schema': 'raw'}

    detection_id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey('fct_messages.message_id'))
    detected_object_class = Column(String)
    confidence_score = Column(Float)

    # Optional: include image_url if it exists in the model
    image_url = Column(String, nullable=True)

    # Relationship
    message = relationship("Message", back_populates="image_detections")
