from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from data_storage.storage import view_mission

from aiogram.types.web_app_info import WebAppInfo

from lexicon.lexicon_buttons import LEXICON_BUTTONS
from lexicon.lexicon_commands import LEXICON_COMMANDS

web_app_button = InlineKeyboardButton(text=LEXICON_COMMANDS['/web_app'][1],
                                      web_app=WebAppInfo(url='https://d0cf-138-199-31-203.ngrok-free.app'))

web_app_kb = InlineKeyboardMarkup(inline_keyboard=[[web_app_button]])

view_button = KeyboardButton(text=LEXICON_BUTTONS['view_button'])
note_button = KeyboardButton(text=LEXICON_BUTTONS['note_button'])
reminder_button = KeyboardButton(text=LEXICON_BUTTONS['reminder_button'])

tools_reply_kb = ReplyKeyboardMarkup(
    keyboard=[[view_button],
              [note_button, reminder_button]],
    resize_keyboard=True
)


def view_missions_keyboard(login):
    kb_sp = []

    for r in view_mission(login):
        kb_sp.append([InlineKeyboardButton(text=f'{r[0]} - {r[1]}', callback_data=LEXICON_BUTTONS['alert'])])
    kb = InlineKeyboardMarkup(inline_keyboard=kb_sp)
    return kb
