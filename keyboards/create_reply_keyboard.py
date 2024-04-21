<<<<<<< HEAD
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon_buttons import LEXICON_BUTTONS


def create_reply_kb(width: int, *args: str, one_time_keyboard: bool = True) -> ReplyKeyboardMarkup:
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = []

    if args:
        for button in args:
            buttons.append(KeyboardButton(
                text=LEXICON_BUTTONS[button] if button in LEXICON_BUTTONS else button))

    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup(resize_keyboard=True,
=======
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon_buttons import LEXICON_BUTTONS


def create_reply_kb(width: int, *args: str, one_time_keyboard: bool = True) -> ReplyKeyboardMarkup:
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = []

    if args:
        for button in args:
            buttons.append(KeyboardButton(
                text=LEXICON_BUTTONS[button] if button in LEXICON_BUTTONS else button))

    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup(resize_keyboard=True,
>>>>>>> origin/master
                                one_time_keyboard=one_time_keyboard)