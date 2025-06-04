import asyncio
import datetime
import logging
import re

from aiogram import (
    Bot,
    Dispatcher,
    F,
    Router,
)
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    Message,
)

import keyboards_builder
from api_methods import (
    chat_user_updated,
    get_discount_payment_order_message,
    get_or_create_chat_user,
    get_second_message,
    get_start_message,
    get_subscribe_offer_message,
    get_third_message,
    get_thirst_payment_order_message,
    get_users_for_payment_notification,
    get_users_for_subscribe_notification,
)
from config import (
    BOT_COMMANDS,
    settings,
)
from constants import (
    EXCEPTION_REPLY_ERROR,
    payment_notification_delay,
    subscribe_offer_notification_delay,
)

router = Router()
bot = Bot(token=settings.bot_token)

dispatcher = Dispatcher()

dispatcher.include_router(router)


@router.message(Command(re.compile(r"^start$")))
async def handle_start(message: Message):
    try:
        start_message = await get_start_message(message.chat.id)
        if not start_message:
            return await message.answer(EXCEPTION_REPLY_ERROR)

        chat_user = await get_or_create_chat_user(
            chat_id=message.chat.id,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
        print(chat_user)
        if not chat_user:
            return await message.answer(EXCEPTION_REPLY_ERROR)

        start_message_texts = start_message["messages"]
        buttons = start_message.get("keyboard")
        keyboard = keyboards_builder.Keyboard(buttons)
        callbacks = start_message.get("callbacks")
        start_message_keyboard = keyboard.build_default_from_buttons_array(
            inline=start_message.get("is_inline", False),
            callbacks=callbacks,
        )
        photos_ids = start_message.get("photos", [])

        if photos_ids:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photos_ids[0],
                caption=start_message_texts[0],
                reply_markup=start_message_keyboard,
            )
        else:
            await message.answer(text=start_message_texts[0], reply_markup=start_message_keyboard)

    except Exception as e:
        logging.error(f"Error during start_message_next_handler: {e}")
        await message.answer(EXCEPTION_REPLY_ERROR)


@router.callback_query(F.data == "start_message_next")
async def second_message_next_handler(callback_query: CallbackQuery):

    message = await get_second_message(callback_query.message.chat.id)

    if not message:
        return await callback_query.answer(EXCEPTION_REPLY_ERROR)

    message_texts = message["messages"]
    buttons = message.get("keyboard")
    keyboard = keyboards_builder.Keyboard(buttons)
    callbacks = message.get("callbacks")
    start_message_keyboard = keyboard.build_default_from_buttons_array(
        inline=message.get("is_inline", False),
        callbacks=callbacks,
    )
    photos_ids = message.get("photos", [])

    if photos_ids:
        await bot.send_photo(
            chat_id=callback_query.message.chat.id,
            photo=photos_ids[0],
            caption=message_texts[0],
            reply_markup=start_message_keyboard,
        )
    else:
        await message.answer(text=message_texts[0], reply_markup=start_message_keyboard)


@router.callback_query(F.data == "second_message_next")
async def third_message_next_handler(callback_query: CallbackQuery):

    message = await get_third_message(callback_query.message.chat.id)

    if not message:
        return await callback_query.answer(EXCEPTION_REPLY_ERROR)

    message_texts = message["messages"]
    buttons = message.get("keyboard")
    keyboard = keyboards_builder.Keyboard(buttons)
    callbacks = message.get("callbacks")
    start_message_keyboard = keyboard.build_default_from_buttons_array(
        inline=message.get("is_inline", False),
        callbacks=callbacks,
    )
    photos_ids = message.get("photos", [])
    if photos_ids:
        await bot.send_photo(
            chat_id=callback_query.message.chat.id,
            photo=photos_ids[0],
            caption=message_texts[0],
            reply_markup=start_message_keyboard,
        )
    else:
        await message.answer(text=message_texts[0], reply_markup=start_message_keyboard)


@router.callback_query(F.data == "pay_button")
async def pay_button_handler(callback_query: CallbackQuery):
    is_updated_response = await chat_user_updated(callback_query.message.chat.id, datetime.datetime.now().isoformat())

    if not is_updated_response or "error" in is_updated_response:
        return await callback_query.answer(EXCEPTION_REPLY_ERROR)

    message = await get_thirst_payment_order_message(callback_query.message.chat.id)

    if not message:
        return await callback_query.answer(EXCEPTION_REPLY_ERROR)

    message_texts = message["messages"]
    buttons = message.get("keyboard")
    keyboard = keyboards_builder.Keyboard(buttons)
    urls = message.get("urls")
    start_message_keyboard = keyboard.build_default_from_buttons_array(
        inline=message.get("is_inline", False),
        urls=urls,
    )
    photos_ids = message.get("photos", [])
    if photos_ids:
        await bot.send_photo(
            chat_id=callback_query.message.chat.id,
            photo=photos_ids[0],
            caption=message_texts[0],
            reply_markup=start_message_keyboard,
        )
    else:
        await message.answer(text=message_texts[0], reply_markup=start_message_keyboard)


async def make_payment_notification():
    while True:
        await asyncio.sleep(payment_notification_delay)

        users = await get_users_for_payment_notification(datetime.datetime.now().isoformat())

        if len(users) == 0:
            logging.info(f"Error during get_users_for_payment_notification: {users}")
            continue

        message = await get_discount_payment_order_message()

        if not message:
            logging.error(f"Error during get_discount_payment_order_message")
            continue

        message_texts = message["messages"]
        buttons = message.get("keyboard")
        keyboard = keyboards_builder.Keyboard(buttons)
        urls = message.get("urls")
        start_message_keyboard = keyboard.build_default_from_buttons_array(
            inline=message.get("is_inline", False),
            urls=urls,
        )
        photos_ids = message.get("photos", [])

        chat_ids = [user["chat_id"] for user in users]

        for chat_id in chat_ids:
            if photos_ids:
                await bot.send_photo(
                    chat_id=chat_id,
                    photo=photos_ids[0],
                    caption=message_texts[0],
                    reply_markup=start_message_keyboard,
                )
            else:
                await bot.send_message(chat_id=chat_id, text=message_texts[0])


async def make_subscribe_offer_notification():
    while True:
        await asyncio.sleep(subscribe_offer_notification_delay)

        users = await get_users_for_subscribe_notification(datetime.datetime.now().isoformat())

        if len(users) == 0:
            logging.info(f"Error during get_users_for_subscribe_notification: {users}")
            continue

        message = await get_subscribe_offer_message()
        message_texts = message["messages"]

        chat_ids = [user["chat_id"] for user in users]

        for chat_id in chat_ids:
            await bot.send_message(chat_id=chat_id, text=message_texts[0])

        if not message:
            logging.error(f"Error during get_subscribe_offer_message")
            continue


async def start_bot():
    logging.basicConfig(
        level=logging.INFO,
        format=settings.log_format,
        datefmt=settings.log_date_format,
        filename=settings.log_path,
        filemode="a",
    )
    await bot.set_my_commands(BOT_COMMANDS)
    coros = [
        make_payment_notification(),
        make_subscribe_offer_notification(),
    ]
    asyncio.gather(*coros)
    await dispatcher.start_polling(bot)


asyncio.run(start_bot())
