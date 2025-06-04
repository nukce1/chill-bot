NEXT_BUTTON = "Далее"
PAY_BUTTON = "Оплатить"
OKAY_NEXT_BUTTON = "Понятно, дальше"
HOW_MUCH_BUTTON = "А cколько стоит?"
CARD_RF_BUTTON = "Карта РФ"
STRIPE_BUTTON = "Stripe (в $)"
LAVA_BUTTON = "Lava (в $)"
HELP_BUTTON = "Служба заботы"


def start_message_keyboard():
    return {
        "NEXT_BUTTON": NEXT_BUTTON,
        "PAY_BUTTON": PAY_BUTTON,
    }


def start_message_callbacks():
    return {
        NEXT_BUTTON: "start_message_next",
        PAY_BUTTON: "pay_button",
    }


def second_message_keyboard():
    return {
        "OKAY_NEXT_BUTTON": OKAY_NEXT_BUTTON,
    }


def second_message_callbacks():
    return {
        OKAY_NEXT_BUTTON: "second_message_next",
    }


def third_message_keyboard():
    return {
        "HOW_MUCH_BUTTON": HOW_MUCH_BUTTON,
    }


def third_message_callbacks():
    return {
        HOW_MUCH_BUTTON: "pay_button",
    }


def thirst_payment_order_message_keyboard():
    return {
        "CARD_RF_BUTTON": CARD_RF_BUTTON,
        "STRIPE_BUTTON": STRIPE_BUTTON,
        "LAVA_BUTTON": LAVA_BUTTON,
        "HELP_BUTTON": HELP_BUTTON,
    }


def thirst_payment_order_message_urls():
    return {
        CARD_RF_BUTTON: "https://github.com/nukce1",
        STRIPE_BUTTON: "https://github.com/nukce1/nebus-testing",
        LAVA_BUTTON: "https://github.com/nukce1/litestar-testing",
        HELP_BUTTON: "https://t.me/chillaibot_bot",
    }
