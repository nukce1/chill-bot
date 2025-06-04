from aiogram import types


class Keyboard:
    def __init__(self, buttons=None):
        if buttons is None:
            buttons = {}
        self.buttons = buttons.values()
        for variable_name, button_name in buttons.items():
            setattr(self, variable_name, button_name)

    def build_default_from_buttons_array(self, callbacks=None, inline: bool = False, urls=None):
        if inline:
            buttons_objs = [
                types.InlineKeyboardButton(
                    text=button_text,
                    callback_data=callbacks.get(button_text, button_text) if callbacks else button_text,
                    url=urls.get(button_text, None) if urls else None,
                )
                for button_text in self.buttons
            ]
            buttons_in_rows = [buttons_objs[i : i + 2] for i in range(0, len(buttons_objs), 2)]
            markup = types.InlineKeyboardMarkup(inline_keyboard=buttons_in_rows)
            return markup

        buttons_objs = [types.KeyboardButton(text=button_text) for button_text in self.buttons]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[buttons_objs])
        return markup
