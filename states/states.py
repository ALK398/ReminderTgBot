from aiogram.filters.state import State, StatesGroup


class FSMStartLogining(StatesGroup):
    start_state = State()
    start_logining_state = State()
    login_state = State()
    password_state = State()
    done_acc_state = State()
    logged_in_state = State()
    view_state = State()
    mission_delete_state = State()

    title_note_state = State()
    description_note_state = State()
    created_note_state = State()

    title_reminder_state = State()
    description_reminder_state = State()
    date_reminder_state = State()
    created_reminder_state = State()

