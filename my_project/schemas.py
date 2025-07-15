# schemas.py
from pydantic import BaseModel
from typing import Optional, List
# schemas.py
from pydantic import BaseModel
from typing import Optional



class TopProductSchema(BaseModel):
    product_name: str
    count: int

    class Config:
        orm_mode = True


class MessageSchema(BaseModel):
    message_id: int
    channel_id: Optional[int]
    date_id: Optional[int]
    message_text: Optional[str]
    message_length: Optional[int]
    has_image: Optional[bool]
    product_name: Optional[str]

    class Config:
        orm_mode = True



class ChannelSchema(BaseModel):
    channel_id: int
    channel_name: str
    channel_type: Optional[str] = None

    class Config:
        orm_mode = True


class DateSchema(BaseModel):
    date_id: int
    date: str
    year: int
    month: int
    day: int
    weekday: str
    week: int

    class Config:
        orm_mode = True



class ImageDetectionSchema(BaseModel):
    detection_id: int
    message_id: int
    detected_object_class: str
    confidence_score: float
    image_url: Optional[str]

    class Config:
        orm_mode = True
