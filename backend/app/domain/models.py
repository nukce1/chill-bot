from typing import Optional

from app.database import Base, created_at, intpk
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.expression import false


class ChatUser(Base):
    __tablename__ = "chat_user"

    id: Mapped[intpk]
    username: Mapped[Optional[str]]
    chat_id: Mapped[int] = mapped_column(unique=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    is_subscribed: Mapped[bool] = mapped_column(default=False)
    is_payed: Mapped[bool] = mapped_column(default=False, server_default=false())
    created_at: Mapped[created_at]
    updated_at: Mapped[created_at]
