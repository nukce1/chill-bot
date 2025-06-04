import datetime
import logging

from app.dependecies.dependencies import get_message_service
from app.domain.schemas import (ChatUserCreationDTO, ChatUserDTO,
                                ChatUserUpdate, ResponseMessageDTO, Timestamp)
from app.services.messages_processor.message_service import MessageService
from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

router = APIRouter(prefix="/core", tags=["core"])


@router.get(
    "/get-start-message",
    response_model=ResponseMessageDTO,
    status_code=HTTP_200_OK,
)
async def get_start_message_handler(
    chat_id: int,
    message_service: MessageService = Depends(get_message_service),
):
    """Get start message for the chat."""
    try:
        return await message_service.get_start_message()
    except Exception as e:
        logging.error(f"Error during get_start_message_handler: {e}")
        raise HTTPException(
            status_code=500, detail="Error during get_start_message_handler"
        )


@router.get(
    "/get-second-message",
    response_model=ResponseMessageDTO,
    status_code=HTTP_200_OK,
)
async def get_second_message_handler(
    chat_id: int,
    message_service: MessageService = Depends(get_message_service),
):
    """Get second message for the chat."""
    try:
        return await message_service.get_second_message(chat_id)
    except Exception as e:
        logging.error(f"Error during get_second_message_handler: {e}")
        raise HTTPException(
            status_code=500, detail="Error during get_second_message_handler"
        )


@router.get(
    "/get-third-message",
    response_model=ResponseMessageDTO,
    status_code=HTTP_200_OK,
)
async def get_third_message_handler(
    chat_id: int,
    message_service: MessageService = Depends(get_message_service),
):
    """Get third message for the chat."""
    try:
        return await message_service.get_third_message(chat_id)
    except Exception as e:
        logging.error(f"Error during get_third_message_handler: {e}")
        raise HTTPException(
            status_code=500, detail="Error during get_third_message_handler"
        )


@router.get(
    "/get-thirst-payment-order-message",
    response_model=ResponseMessageDTO,
    status_code=HTTP_200_OK,
)
async def get_thirst_payment_order_message_handler(
    chat_id: int,
    message_service: MessageService = Depends(get_message_service),
):
    """Get thirst payment order message for the chat."""
    try:
        return await message_service.get_thirst_payment_order_message(chat_id)
    except Exception as e:
        logging.error(f"Error during get_thirst_payment_order_message_handler: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error during get_thirst_payment_order_message_handler",
        )


@router.post(
    "/get-or-create-chat-user",
    response_model=ChatUserDTO,
    status_code=HTTP_201_CREATED,
)
async def get_or_create_chat_user_handler(
    chat_user_creation_dto: ChatUserCreationDTO,
    message_service: MessageService = Depends(get_message_service),
):
    """Get or create chat user in the database."""
    try:
        return await message_service.get_or_create_chat_user(chat_user_creation_dto)
    except Exception as e:
        logging.error(f"Error during get_or_create_chat_user_handler: {e}")
        raise HTTPException(
            status_code=500, detail="Error during get_or_create_chat_user_handler"
        )


@router.post(
    "/chat-user-updated",
    status_code=HTTP_200_OK,
)
async def chat_user_updated_handler(
    chat_user_update: ChatUserUpdate,
    message_service: MessageService = Depends(get_message_service),
):
    """Update chat user timestamp."""
    try:
        return await message_service.chat_user_updated(chat_user_update)
    except Exception as e:
        logging.error(f"Error during chat_user_updated_handler: {e}")
        raise HTTPException(
            status_code=500, detail="Error during chat_user_updated_handler"
        )


@router.post(
    "/get-users-for-payment-notification",
    response_model=list[ChatUserDTO],
    status_code=HTTP_200_OK,
)
async def get_users_for_payment_notification_handler(
    timestamp: Timestamp,
    message_service: MessageService = Depends(get_message_service),
):
    """Get users for payment notification."""
    try:
        return await message_service.get_users_for_payment_notification(timestamp)
    except Exception as e:
        logging.error(f"Error during get_users_for_payment_notification_handler: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error during get_users_for_payment_notification_handler",
        )


@router.get(
    "/get-discount-payment-order-message",
    response_model=ResponseMessageDTO,
    status_code=HTTP_200_OK,
)
async def get_discount_payment_order_message_handler(
    message_service: MessageService = Depends(get_message_service),
):
    """Get discount payment order message for the chat."""
    try:
        return await message_service.get_discount_payment_order_message()
    except Exception as e:
        logging.error(f"Error during get_discount_payment_order_message_handler: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error during get_discount_payment_order_message_handler",
        )


@router.post(
    "/get-users-for-subscribe-notification",
    response_model=list[ChatUserDTO],
    status_code=HTTP_200_OK,
)
async def get_users_for_subscribe_notification_handler(
    timestamp: Timestamp,
    message_service: MessageService = Depends(get_message_service),
):
    """Get users for subscribe notification."""
    try:
        return await message_service.get_users_for_subscribe_notification(timestamp)
    except Exception as e:
        logging.error(f"Error during get_users_for_subscribe_notification_handler: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error during get_users_for_subscribe_notification_handler",
        )


@router.get(
    "/get-subscribe-offer-message",
    response_model=ResponseMessageDTO,
    status_code=HTTP_200_OK,
)
async def get_subscribe_offer_message_handler(
    message_service: MessageService = Depends(get_message_service),
):
    """Get subscribe offer message for the chat."""
    try:
        return await message_service.get_subscribe_offer_message()
    except Exception as e:
        logging.error(f"Error during get_subscribe_offer_message_handler: {e}")
        raise HTTPException(
            status_code=500, detail="Error during get_subscribe_offer_message_handler"
        )
