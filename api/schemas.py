# schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
# schemas.py
from pydantic import BaseModel
from typing import Optional



class TopProductSchema(BaseModel):
    product_name: str
    count: int

    class Config:
      from_attributes = True



class MessageSchema(BaseModel):
    message_id: int
    channel_name: Optional[str]
    message_date: Optional[datetime]
    message_text: Optional[str]
    message_length: Optional[int]
    has_image: Optional[bool]
    product_name: Optional[str]

    class Config:
      from_attributes = True



class ChannelSchema(BaseModel):
    channel_name: str
  


class DateSchema(BaseModel):
    date_id: int
    date: str
    year: int
    month: int
    day: int
    weekday: str
    week: int

    class Config:
      from_attributes = True




class ImageDetectionSchema(BaseModel):
    detection_id: int
    message_id: int
    detected_object_class: str
    confidence_score: float
    image_url: Optional[str]

    class Config:
       from_attributes = True
