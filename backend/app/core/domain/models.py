from typing import Optional

from sqlalchemy.orm import (
    Mapped,
    mapped_column, relationship,
)

from backend.config import settings
from backend.database import (
    Base,
    created_at,
    intpk,
)


class User(Base):
    __tablename__ = "user"

    id: Mapped[intpk]
    name: Mapped[str]
    created_at: Mapped[created_at]

    chat_users = relationship("ChatUser", back_populates="user")


class ChatUser(Base):
    __tablename__ = "chat_user"

    id: Mapped[intpk]
    username: Mapped[Optional[str]]
    chat_id: Mapped[int] = mapped_column(unique=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    state: Mapped[Optional[int]] = mapped_column(default=0)
    step: Mapped[Optional[int]] = mapped_column(default=0)
    template_uses_count: Mapped[int] = mapped_column(default=settings.free_template_uses_count)
    created_at: Mapped[created_at]

    user = relationship(User, back_populates="chat_users")

class UserMessage(Base):
    __tablename__ = "user_message"

    id: Mapped[intpk]
    chat_id: Mapped[int]
    chat_user_id: Mapped[int]
    telegram_message_id: Mapped[int]
    text: Mapped[str]
    created_at: Mapped[created_at]
