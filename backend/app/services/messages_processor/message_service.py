import datetime
import logging

from app.domain.schemas import (ChatUserCreationDTO, ChatUserUpdate,
                                ResponseMessageDTO, Timestamp, UserCreationDTO)
from app.repositories.postgres_repo import PostgresStorage
from app.services.messages_processor.constants import (
    discount_payment_order_message_photos_ids,
    discount_payment_order_message_text, second_message_photos_ids,
    second_message_text, start_message_photos_ids, start_message_text,
    subscribe_offer_message_text, third_message_photos_ids, third_message_text,
    thirst_payment_order_message_photos_ids, thirst_payment_order_message_text)
from app.services.messages_processor.keyboards import (
    second_message_callbacks, second_message_keyboard, start_message_callbacks,
    start_message_keyboard, third_message_callbacks, third_message_keyboard,
    thirst_payment_order_message_keyboard, thirst_payment_order_message_urls)


class MessageService:
    def __init__(self, storage: PostgresStorage):
        logging.info("MessageService init")
        self.storage = storage

    @staticmethod
    async def get_start_message():
        """Get start message for the chat."""
        response = ResponseMessageDTO(
            messages=[start_message_text],
            keyboard=start_message_keyboard(),
            callbacks=start_message_callbacks(),
            urls=None,
            is_inline=True,
            photos=start_message_photos_ids,
        )
        return response.model_dump()

    @staticmethod
    async def get_second_message(chat_id: int):
        """Get second message for the chat."""
        response = ResponseMessageDTO(
            messages=[second_message_text],
            keyboard=second_message_keyboard(),
            callbacks=second_message_callbacks(),
            urls=None,
            is_inline=True,
            photos=second_message_photos_ids,
        )
        return response.model_dump()

    @staticmethod
    async def get_third_message(chat_id: int):
        """Get third message for the chat."""
        response = ResponseMessageDTO(
            messages=[third_message_text],
            keyboard=third_message_keyboard(),
            callbacks=third_message_callbacks(),
            urls=None,
            is_inline=True,
            photos=third_message_photos_ids,
        )
        return response.model_dump()

    @staticmethod
    async def get_thirst_payment_order_message(chat_id: int):
        """Get thirst payment order message for the chat."""
        response = ResponseMessageDTO(
            messages=[thirst_payment_order_message_text],
            keyboard=thirst_payment_order_message_keyboard(),
            callbacks=None,
            urls=thirst_payment_order_message_urls(),
            is_inline=True,
            photos=thirst_payment_order_message_photos_ids,
        )
        return response.model_dump()

    @staticmethod
    async def get_discount_payment_order_message():
        """Get discount payment order message for the chat."""
        response = ResponseMessageDTO(
            messages=[discount_payment_order_message_text],
            keyboard=thirst_payment_order_message_keyboard(),
            callbacks=None,
            urls=thirst_payment_order_message_urls(),
            is_inline=True,
            photos=discount_payment_order_message_photos_ids,
        )
        return response.model_dump()

    @staticmethod
    async def get_subscribe_offer_message():
        """Get subscribe offer message for the chat."""
        response = ResponseMessageDTO(
            messages=[subscribe_offer_message_text],
            keyboard=None,
            callbacks=None,
            urls=None,
            is_inline=True,
            photos=None,
        )
        return response.model_dump()

    async def get_or_create_chat_user(
        self, chat_user_creation_dto: ChatUserCreationDTO
    ):
        """Get or create chat user in the database."""
        chat_user = await self.storage.get_chat_user_by_telegram_id(
            chat_user_creation_dto.telegram_id
        )

        if chat_user:
            return chat_user.model_dump()

        chat_user = await self.storage.create_chat_user(chat_user_creation_dto)

        return chat_user.model_dump()

    async def chat_user_updated(self, chat_user_update: ChatUserUpdate):
        """Update chat user timestamp."""
        chat_user = await self.storage.get_chat_user_by_telegram_id(
            chat_user_update.chat_id
        )
        print(chat_user)

        if not chat_user:
            return {"error": "Chat user not found"}

        is_updated = await self.storage.update_chat_user_updated_at(
            chat_user, chat_user_update.timestamp
        )
        if not is_updated:
            return {"error": "Chat user not updated"}

        return {"detail": "Chat user updated"}

    async def get_users_for_payment_notification(self, timestamp: Timestamp):
        """Get users for payment notification."""
        users = await self.storage.get_users_for_payment_notification(timestamp)

        return users if users else []

    async def get_users_for_subscribe_notification(self, timestamp: Timestamp):
        """Get users for subscribe notification."""
        users = await self.storage.get_users_for_subscribe_notification(timestamp)

        return users if users else []
