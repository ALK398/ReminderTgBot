import asyncio

from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.state import default_state

from data_storage import storage
from data_storage import session_info

from keyboards.create_reply_keyboard import create_reply_kb
from keyboards.keyboards import tools_reply_kb, view_missions_keyboard
from keyboards.keyboards import web_app_kb

from lexicon.lexicon_answers import LEXICON_ANSWERS
from lexicon.lexicon_buttons import LEXICON_BUTTONS
from lexicon.lexicon_commands import LEXICON_COMMANDS

from states.states import FSMStartLogining

router_logging = Router()


@router_logging.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_COMMANDS['/start'][1],
                         reply_markup=create_reply_kb(1, LEXICON_BUTTONS['good_button']))
    await state.set_state(FSMStartLogining.start_state)


@router_logging.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_COMMANDS['/help'][1])


@router_logging.message(Command(commands='log_out'), StateFilter(FSMStartLogining.logged_in_state))
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
    session_info.fill_login(message.from_user.username, str(message.text))
    await state.set_state(FSMStartLogining.password_state)


@router_logging.message(StateFilter(FSMStartLogining.password_state), lambda x: ' ' not in x.text and '/' not in x.text)
async def process_logged_in_command(message: Message, state: FSMContext):
    await message.answer(text='Проверяю данные...',
                         reply_markup=create_reply_kb(1, LEXICON_BUTTONS['ok_button']))
    session_info.fill_password(message.from_user.username, str(message.text))
    await state.set_state(FSMStartLogining.done_acc_state)


@router_logging.message(StateFilter(FSMStartLogining.done_acc_state), lambda x: len(x.text.split()) < 2)
async def process_good_answer(message: Message, state: FSMContext):
    login = session_info.read_info(message.from_user.username, 'login')
    password = session_info.read_info(message.from_user.username, 'password')
    if not storage.search_login(login):
        storage.anaot(login, password)
        await message.answer(text='Вы создали новый аккаунт!', reply_markup=tools_reply_kb)
        await state.set_state(FSMStartLogining.logged_in_state)
    if storage.search_password(login, password):
        await message.answer(text='Вы вошли в аккаунт!', reply_markup=tools_reply_kb)
        await state.set_state(FSMStartLogining.logged_in_state)
    if not storage.search_password(login, password):
        await message.answer(text='Неверный логин или пароль! (введите: "ЛОГИН ПАРОЛЬ", через пробел)')


@router_logging.message(StateFilter(FSMStartLogining.done_acc_state), lambda x: len(x.text.split()) == 2)
async def process_good_answer(message: Message, state: FSMContext):
    if storage.search_password((str(message.text)).split()[0], (str(message.text)).split()[1]):
        session_info.fill_login(message.from_user.username, (str(message.text)).split()[0])
        session_info.fill_password(message.from_user.username, (str(message.text)).split()[1])
        await message.answer(text='Вы вошли в аккаунт!', reply_markup=tools_reply_kb)
        await state.set_state(FSMStartLogining.logged_in_state)
    else:
        await message.answer(text='Вы вписали что-то неверное')


@router_logging.message(Command(commands='web_app'), StateFilter(FSMStartLogining.logged_in_state))
async def process_web_app(message: Message):
    await message.answer(text=LEXICON_COMMANDS['/web_app'][0], reply_markup=web_app_kb)


@router_logging.message(F.text == LEXICON_BUTTONS['view_button'], StateFilter(FSMStartLogining.logged_in_state))
async def view_message(message: Message, state: FSMContext):
    login = session_info.read_info(message.from_user.username, 'login')
    await message.answer(
        text='Список Задач:',
        reply_markup=view_missions_keyboard(login))
    await message.answer(text='.', reply_markup=create_reply_kb(2, 'Удалить', 'Назад'))
    await state.set_state(FSMStartLogining.view_state)


@router_logging.message(F.text == 'Назад', StateFilter(FSMStartLogining.view_state))
async def view_back_message(message: Message, state: FSMContext):
    await message.answer(text='.', reply_markup=tools_reply_kb)
    await state.set_state(FSMStartLogining.logged_in_state)


@router_logging.message(F.text == 'Удалить', StateFilter(FSMStartLogining.view_state))
async def view_delete_message(message: Message, state: FSMContext):
    await message.answer(text='Впишите название задачи, которое вы хотите удалить')
    await state.set_state(FSMStartLogining.mission_delete_state)


@router_logging.message(StateFilter(FSMStartLogining.mission_delete_state))
async def view_delete_message_process(message: Message, state: FSMContext):
    login = session_info.read_info(message.from_user.username, 'login')
    storage.delete_mission(login, message.text)
    await message.answer(text=f'вы удалили задачу с названием {message.text}', reply_markup=tools_reply_kb)
    await state.set_state(FSMStartLogining.logged_in_state)


router_note = Router()


@router_note.message(F.text == LEXICON_BUTTONS['note_button'], StateFilter(FSMStartLogining.logged_in_state))
async def process_note_answer(message: Message, state: FSMContext):
    await message.answer(text='Отправьте название Заметки', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMStartLogining.title_note_state)


@router_note.message(StateFilter(FSMStartLogining.title_note_state))
async def process_note_title(message: Message, state: FSMContext):
    session_info.fill_mission_type(message.from_user.username, 'note')
    session_info.fill_mission_title(message.from_user.username, str(message.text))
    await message.answer(text='Отправьте описание Заметки')
    await state.set_state(FSMStartLogining.description_note_state)


@router_note.message(StateFilter(FSMStartLogining.description_note_state))
async def process_note_description(message: Message, state: FSMContext):
    session_info.fill_mission_description(message.from_user.username, str(message.text))
    await message.answer(text='Вы создали Заметку!', reply_markup=create_reply_kb(1, LEXICON_BUTTONS['ok_button']))
    await state.set_state(FSMStartLogining.created_note_state)


@router_note.message(StateFilter(FSMStartLogining.created_note_state))
async def process_note_created(message: Message, state: FSMContext):
    note_title = session_info.read_info(message.from_user.username, 'mission_title')
    note_description = session_info.read_info(message.from_user.username, 'mission_description')
    login = session_info.read_info(message.from_user.username, 'login')
    storage.antot(login, 'note', note_title, note_description)
    await message.answer(text='Готово!', reply_markup=tools_reply_kb)
    await state.set_state(FSMStartLogining.logged_in_state)


router_reminder = Router()


@router_reminder.message(F.text == LEXICON_BUTTONS['reminder_button'], StateFilter(FSMStartLogining.logged_in_state))
async def process_reminder_answer(message: Message, state: FSMContext):
    await message.answer(text='Отправьте название Напоминания', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMStartLogining.title_reminder_state)


@router_reminder.message(StateFilter(FSMStartLogining.title_reminder_state))
async def process_reminder_title(message: Message, state: FSMContext):
    session_info.fill_mission_type(message.from_user.username, 'reminder')
    session_info.fill_mission_title(message.from_user.username, str(message.text))
    await message.answer(text='Отправьте описание Напоминания')
    await state.set_state(FSMStartLogining.description_reminder_state)


@router_reminder.message(StateFilter(FSMStartLogining.description_reminder_state))
async def process_reminder_description(message: Message, state: FSMContext):
    session_info.fill_mission_description(message.from_user.username, str(message.text))
    await message.answer(text='Отправьте дату и время Напоминания форматом: "ГГГГ-ММ-ДД ЧЧ:ММ"')
    await state.set_state(FSMStartLogining.date_reminder_state)


@router_reminder.message(StateFilter(FSMStartLogining.date_reminder_state),
                         lambda x: len(x.text) == 16)
async def process_reminder_datec(message: Message, state: FSMContext):
    session_info.fill_mission_date(message.from_user.username, str(message.text))
    await message.answer(text='Вы создали Напоминание!', reply_markup=create_reply_kb(1, LEXICON_BUTTONS['ok_button']))
    await state.set_state(FSMStartLogining.created_reminder_state)


@router_reminder.message(StateFilter(FSMStartLogining.created_reminder_state))
async def process_reminder_created(message: Message, state: FSMContext):
    reminder_title = session_info.read_info(message.from_user.username, 'mission_title')
    reminder_description = session_info.read_info(message.from_user.username, 'mission_description')
    reminder_date = session_info.read_info(message.from_user.username, 'mission_date')
    login = session_info.read_info(message.from_user.username, 'login')
    storage.antot(login, 'reminder', reminder_title, reminder_description, reminder_date, message.chat.id)
    await message.answer(text='Готово!', reply_markup=tools_reply_kb)
    await state.set_state(FSMStartLogining.logged_in_state)


@router_reminder.message(StateFilter(FSMStartLogining.logged_in_state))
async def check_reminder(bot):
    reminders = storage.check_reminders()
    if reminders:
        for rem in reminders:
            await bot.send_message(rem[-1], f'НАПОМИНАНИЕ:\n{rem[0]} - {rem[1]}')
    await asyncio.sleep(60)
