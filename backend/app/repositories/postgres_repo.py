import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import ChatUser
from app.domain.schemas import ChatUserDTO, ChatUserCreationDTO, Timestamp


class PostgresStorage:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_chat_user_by_telegram_id(self, telegram_id: int) -> ChatUserDTO | None:
        """Get chat user by telegram id."""
        query = select(ChatUser).where(ChatUser.telegram_id == telegram_id)
        result = await self.session.execute(query)
        chat_user_orm: ChatUser = result.scalar_one_or_none()

        if chat_user_orm:
            return ChatUserDTO.model_validate(chat_user_orm)


    async def create_chat_user(self, chat_user: ChatUserCreationDTO) -> ChatUserDTO:
        """Create chat user."""
        chat_user_orm = ChatUser(**chat_user.model_dump())

        self.session.add(chat_user_orm)
        await self.session.commit()

        return ChatUserDTO.model_validate(chat_user_orm)


    async def update_chat_user_updated_at(self, chat_user: ChatUserDTO, timestamp: datetime) -> bool:
        """Update chat user timestamp."""
        query = (
            update(ChatUser)
            .where(ChatUser.telegram_id == chat_user.telegram_id)
            .values(
                id=chat_user.id,
                updated_at=timestamp
            )
        )

        result = await self.session.execute(query)
        await self.session.commit()

        return result.rowcount > 0

    async def get_users_for_payment_notification(self, tmstp: Timestamp) -> list[ChatUserDTO] | None:
        """Get users for payment notification."""
        adjusted_timestamp_lower = tmstp.timestamp - datetime.timedelta(minutes=15)
        query = (
            select(ChatUser)
            .where(ChatUser.is_payed == False)
            .where(ChatUser.updated_at.between(adjusted_timestamp_lower, tmstp.timestamp))
            .order_by(ChatUser.updated_at.desc())
        )

        result = await self.session.execute(query)
        chat_users_orm: list[ChatUser] = result.scalars().all()

        if chat_users_orm:
            return [ChatUserDTO.model_validate(chat_user_orm) for chat_user_orm in chat_users_orm]

    async def get_users_for_subscribe_notification(self, tmstp: Timestamp) -> list[ChatUserDTO] | None:
        """Get users for subscribe notification."""
        adjusted_timestamp_lower = tmstp.timestamp - datetime.timedelta(minutes=15)
        query = (
            select(ChatUser)
            .where(ChatUser.is_subscribed == False)
            .where(ChatUser.updated_at.between(adjusted_timestamp_lower, tmstp.timestamp))
            .order_by(ChatUser.updated_at.desc())
        )

        result = await self.session.execute(query)
        chat_users_orm: list[ChatUser] = result.scalars().all()

        if chat_users_orm:
            return [ChatUserDTO.model_validate(chat_user_orm) for chat_user_orm in chat_users_orm]