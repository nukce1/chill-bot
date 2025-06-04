import datetime
from urllib.parse import urlencode

import httpx

from config import settings


async def api_request(method: str, path: str, params: dict = None, data: dict = None, json: dict = None):
    """Makes an async request to the backend API."""
    url = settings.backend_url + path
    if params:
        url += "?" + urlencode(params)

    async with httpx.AsyncClient() as client:
        response = await client.request(method, url, data=data, json=json)

        if response.status_code == 200 or response.status_code == 201:
            return response.json()

        return None


async def get_start_message(chat_id: int):
    """Get start message for the chat."""
    return await api_request("GET", f"/api/v1/core/get-start-message", params={"chat_id": chat_id})


async def get_or_create_chat_user(chat_id: int, telegram_id: int, username=None, first_name=None, last_name=None):
    """Get or create chat user in the database."""
    return await api_request(
        "POST",
        f"/api/v1/core/get-or-create-chat-user",
        json={
            "chat_id": chat_id,
            "telegram_id": telegram_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
        },
    )


async def get_second_message(chat_id: int):
    """Get second message for the chat."""
    return await api_request("GET", f"/api/v1/core/get-second-message", params={"chat_id": chat_id})


async def get_third_message(chat_id: int):
    """Get third message for the chat."""
    return await api_request("GET", f"/api/v1/core/get-third-message", params={"chat_id": chat_id})


async def get_thirst_payment_order_message(chat_id: int):
    """Get payments message for the chat."""
    return await api_request("GET", f"/api/v1/core/get-thirst-payment-order-message", params={"chat_id": chat_id})


async def chat_user_updated(chat_id: int, timestamp: datetime):
    """Update chat user timestamp."""
    return await api_request(
        "POST", f"/api/v1/core/chat-user-updated", json={"chat_id": chat_id, "timestamp": timestamp}
    )


async def get_users_for_payment_notification(timestamp: datetime):
    """Get users for payment notification."""
    return await api_request("POST", f"/api/v1/core/get-users-for-payment-notification", json={"timestamp": timestamp})


async def get_discount_payment_order_message():
    """Get discount payment order message for the chat."""
    return await api_request("GET", f"/api/v1/core/get-discount-payment-order-message")


async def get_users_for_subscribe_notification(timestamp: datetime):
    """Get users for subscribe notification."""
    return await api_request(
        "POST", f"/api/v1/core/get-users-for-subscribe-notification", json={"timestamp": timestamp}
    )

async def get_subscribe_offer_message():
    """Get subscribe offer message for the chat."""
    return await api_request("GET", f"/api/v1/core/get-subscribe-offer-message")
