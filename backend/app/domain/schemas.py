from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ChatUserGetDTO(BaseModel):
    id: int


class ChatUserCreationDTO(BaseModel):
    chat_id: int
    telegram_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class ChatUserDTO(BaseModel):
    id: int
    username: Optional[str]
    chat_id: int
    telegram_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    is_subscribed: bool
    is_payed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatUserUpdate(BaseModel):
    chat_id: int
    timestamp: datetime


class UserCreationDTO(BaseModel):
    chat_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class ResponseMessageDTO(BaseModel):
    messages: list[str]
    keyboard: Optional[dict]
    callbacks: Optional[dict]
    urls: Optional[dict]
    is_inline: Optional[bool]
    photos: Optional[list[str]]

    model_config = ConfigDict(from_attributes=True)


class Timestamp(BaseModel):
    timestamp: datetime
