import random

from lexicon.lexicon_buttons import LEXICON_BUTTONS


# Функция, возвращающая случайный выбор бота в игре
def get_bot_choice() -> str:
    return random.choice(['rock_button', 'paper_button', 'scissors_button'])


# Функция, возвращающая ключ из словаря, по которому
# хранится значение, передаваемое как аргумент - выбор пользователя
def _normalize_user_answer(user_answer: str) -> str:
    for key in LEXICON_BUTTONS:
        if LEXICON_BUTTONS[key] == user_answer:
            break
    return key


# Функция, определяющая победителя
def get_winner(user_choice: str, bot_choice: str) -> str:
    user_choice = _normalize_user_answer(user_choice)
    rules = {'rock_button': 'scissors_button',
             'scissors_button': 'paper_button',
             'paper_button': 'rock_button'}
    if user_choice == bot_choice:
        return 'nobody_won'
    elif rules[user_choice] == bot_choice:
        return 'user_won'
    return 'bot_won'
