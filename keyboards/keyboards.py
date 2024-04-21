from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from lexicon.lexicon_buttons import LEXICON_BUTTONS
from lexicon.lexicon_commands import LEXICON_COMMANDS

from keyboards.create_reply_keyboard import create_reply_kb

create_button = KeyboardButton(text=LEXICON_BUTTONS['create_button'])
note_button = KeyboardButton(text=LEXICON_BUTTONS['note_button'])
reminder_button = KeyboardButton(text=LEXICON_BUTTONS['reminder_button'])
task_button = KeyboardButton(text=LEXICON_BUTTONS['task_button'])

tools_reply_kb = ReplyKeyboardMarkup(
    keyboard=[[create_button],
              [note_button, reminder_button, task_button]],
    resize_keyboard=True
)
