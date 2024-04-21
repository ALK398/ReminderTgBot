from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import default_state

from data_storage import storage

from keyboards.create_reply_keyboard import create_reply_kb
from keyboards.keyboards import tools_reply_kb

from lexicon.lexicon_answers import LEXICON_ANSWERS
from lexicon.lexicon_buttons import LEXICON_BUTTONS
from lexicon.lexicon_commands import LEXICON_COMMANDS

from states.states import FSMStartLogining

router_logging = Router()

login = ''
password = ''

note_title = ''
note_description = ''

reminder_title = ''
reminder_description = ''
reminder_date = ''

task_title = ''
task_description = ''
task_date = ''
task_status = ''


@router_logging.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_COMMANDS['/start'][1],
                         reply_markup=create_reply_kb(1, LEXICON_BUTTONS['good_button']))
    await state.set_state(FSMStartLogining.start_state)


@router_logging.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_COMMANDS['/help'][1])


@router_logging.message(Command(commands='log_out'), F.text == LEXICON_COMMANDS['/log_out'][1],
                        StateFilter(FSMStartLogining.logged_in_state))
async def process_log_out_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_COMMANDS['/log_out'][1], reply_markup=ReplyKeyboardRemove())
    await state.set_state(default_state)


@router_logging.message(F.text == LEXICON_BUTTONS['good_button'], StateFilter(FSMStartLogining.start_state))
async def process_good_answer(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_COMMANDS['/log_in'][1],
                         reply_markup=create_reply_kb(1, LEXICON_COMMANDS['/log_in'][0]))
    await state.set_state(FSMStartLogining.start_logining_state)


@router_logging.message(StateFilter(FSMStartLogining.start_logining_state))
async def process_login_answer(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_ANSWERS['login'], reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMStartLogining.login_state)


@router_logging.message(StateFilter(FSMStartLogining.login_state), lambda x: ' ' not in x.text and '/' not in x.text)
async def process_password_answer(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_ANSWERS['password'])
    global login
    login = message.text
    await state.set_state(FSMStartLogining.password_state)


@router_logging.message(StateFilter(FSMStartLogining.password_state), lambda x: ' ' not in x.text and '/' not in x.text)
async def process_logged_in_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_ANSWERS['logged_in'], reply_markup=create_reply_kb(1, LEXICON_BUTTONS['ok_button']))
    global password
    password = message.text
    await state.set_state(FSMStartLogining.done_acc_state)


@router_logging.message(StateFilter(FSMStartLogining.done_acc_state))
async def process_good_answer(message: Message, state: FSMContext):
    await message.answer(text='Готово!', reply_markup=tools_reply_kb)
    global login, password
    storage.anaot(login, password)
    await state.set_state(FSMStartLogining.logged_in_state)


@router_logging.message(F.text == LEXICON_BUTTONS['create_button'], StateFilter(FSMStartLogining.logged_in_state))
async def process_good_answer(message: Message):
    global login
    t = storage.view_missions(login)
    t = '\n\n'.join(t)
    await message.answer(text=t)


router_note = Router()


@router_note.message(F.text == LEXICON_BUTTONS['note_button'], StateFilter(FSMStartLogining.logged_in_state))
async def process_note_answer(message: Message, state: FSMContext):
    await message.answer(text='Отправьте название Заметки', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMStartLogining.title_note_state)


@router_note.message(StateFilter(FSMStartLogining.title_note_state))
async def process_note_title(message: Message, state: FSMContext):
    global note_title
    note_title = message.text
    await message.answer(text='Отправьте описание Заметки')
    await state.set_state(FSMStartLogining.description_note_state)


@router_note.message(StateFilter(FSMStartLogining.description_note_state))
async def process_note_description(message: Message, state: FSMContext):
    global note_description
    note_description = message.text
    await message.answer(text='Вы создали Заметку!', reply_markup=create_reply_kb(1, LEXICON_BUTTONS['ok_button']))
    await state.set_state(FSMStartLogining.created_note_state)


@router_note.message(StateFilter(FSMStartLogining.created_note_state))
async def process_note_created(message: Message, state: FSMContext):
    global note_description, note_title, login
    storage.antot(login, 'note', note_title, note_description)
    note_title, note_description = '', ''
    await message.answer(text='Готово!', reply_markup=tools_reply_kb)
    await state.set_state(FSMStartLogining.logged_in_state)


router_reminder = Router()


@router_reminder.message(F.text == LEXICON_BUTTONS['reminder_button'], StateFilter(FSMStartLogining.logged_in_state))
async def process_reminder_answer(message: Message, state: FSMContext):
    await message.answer(text='Отправьте название Напоминания', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMStartLogining.title_reminder_state)


@router_reminder.message(StateFilter(FSMStartLogining.title_reminder_state))
async def process_reminder_title(message: Message, state: FSMContext):
    global reminder_title
    reminder_title = message.text
    await message.answer(text='Отправьте описание Напоминания')
    await state.set_state(FSMStartLogining.description_reminder_state)


@router_reminder.message(StateFilter(FSMStartLogining.description_reminder_state))
async def process_reminder_description(message: Message, state: FSMContext):
    global reminder_description
    reminder_description = message.text
    await message.answer(text='Отправьте дату и время Напоминания форматом: "ДЕНЬ/МЕСЯЦ/ГОД/ЧАС/МИНУТА"')
    await state.set_state(FSMStartLogining.date_reminder_state)


@router_reminder.message(StateFilter(FSMStartLogining.date_reminder_state))
async def process_reminder_datec(message: Message, state: FSMContext):
    global reminder_date
    reminder_date = message.text
    await message.answer(text='Вы создали Напоминание!', reply_markup=create_reply_kb(1, LEXICON_BUTTONS['ok_button']))
    await state.set_state(FSMStartLogining.created_reminder_state)


@router_reminder.message(StateFilter(FSMStartLogining.created_reminder_state))
async def process_reminder_created(message: Message, state: FSMContext):
    global reminder_description, reminder_title, reminder_date, login
    storage.antot(login, 'reminder', reminder_title, reminder_description, reminder_date)
    reminder_title, reminder_description, reminder_date = '', '', ''
    await message.answer(text='Готово!', reply_markup=tools_reply_kb)
    await state.set_state(FSMStartLogining.logged_in_state)


router_task = Router()


@router_task.message(F.text == LEXICON_BUTTONS['task_button'], StateFilter(FSMStartLogining.logged_in_state))
async def process_task_answer(message: Message, state: FSMContext):
    await message.answer(text='Отправьте название Задачи', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMStartLogining.title_task_state)


@router_task.message(StateFilter(FSMStartLogining.title_task_state))
async def process_task_title(message: Message, state: FSMContext):
    global task_title
    task_title = message.text
    await message.answer(text='Отправьте описание Задачи')
    await state.set_state(FSMStartLogining.description_task_state)


@router_task.message(StateFilter(FSMStartLogining.description_task_state))
async def process_task_description(message: Message, state: FSMContext):
    global task_description
    task_description = message.text
    await message.answer(text='Отправьте дату Задачи форматом: "ДЕНЬ/МЕСЯЦ/ГОД/ЧАС/МИНУТА"')
    await state.set_state(FSMStartLogining.date_task_state)


@router_task.message(StateFilter(FSMStartLogining.date_task_state))
async def process_task_datec(message: Message, state: FSMContext):
    global task_date
    task_date = message.text
    await message.answer(text='Вы создали Задачу!', reply_markup=create_reply_kb(1, LEXICON_BUTTONS['ok_button']))
    await state.set_state(FSMStartLogining.created_task_state)


@router_task.message(StateFilter(FSMStartLogining.created_task_state))
async def process_task_created(message: Message, state: FSMContext):
    global task_description, task_title, task_date, login
    storage.antot(login, 'task', task_title, task_description, task_date)
    task_title, task_description, task_date = '', '', ''
    await message.answer(text='Готово!', reply_markup=tools_reply_kb)
    await state.set_state(FSMStartLogining.logged_in_state)
