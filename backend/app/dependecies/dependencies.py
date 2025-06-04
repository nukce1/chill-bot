from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.repositories.postgres_repo import PostgresStorage
from app.services.messages_processor.message_service import MessageService


def get_storage(session: Annotated[AsyncSession, Depends(get_db_session)]) -> PostgresStorage:
    return PostgresStorage(session=session)

def get_message_service(storage: Annotated[PostgresStorage, Depends(get_storage)]) -> MessageService:
    return MessageService(storage=storage)