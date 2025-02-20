from aiogram.fsm.state import StatesGroup, State


class HomeworkStates(StatesGroup):
    AWAITING_SCHOOL = State()
    AWAITING_CLASS = State()
    AWAITING_SUBJECT = State()
    AWAITING_TEXT = State()
    GETTING_SCHOOL = State()
    GETTING_CLASS = State()
    GETTING_SUBJECT = State()