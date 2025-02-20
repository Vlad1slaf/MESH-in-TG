from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from services.database import get_homework, update_homework
from services.logger import logger
from bot.states.homework import HomeworkStates
from bot.keyboards.builders import cancel_keyboard, subject_keyboard

router = Router()


@router.message(Command("add_hw"))
async def hw_command(message: Message, state: FSMContext):
    await message.answer("Введите номер школы:", reply_markup=cancel_keyboard())
    await state.set_state(HomeworkStates.AWAITING_SCHOOL)


@router.message(HomeworkStates.AWAITING_SCHOOL, F.text.regexp(r'^\d+$'))
async def process_school(message: Message, state: FSMContext):
    await state.update_data(school_id=int(message.text))
    await message.answer("Введите класс (например, 10A):", reply_markup=cancel_keyboard())
    await state.set_state(HomeworkStates.AWAITING_CLASS)


@router.message(HomeworkStates.AWAITING_CLASS)
async def process_class(message: Message, state: FSMContext):
    await state.update_data(class_name=message.text.upper())
    await message.answer("Введите предмет:", reply_markup=subject_keyboard())
    await state.set_state(HomeworkStates.AWAITING_SUBJECT)


@router.message(HomeworkStates.AWAITING_SUBJECT, F.text)
async def process_subject(message: Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await message.answer("Введите текст домашнего задания:", reply_markup=cancel_keyboard())  # Запрашиваем текст
    await state.set_state(HomeworkStates.AWAITING_TEXT)


@router.message(HomeworkStates.AWAITING_TEXT, F.text)
async def process_text(message: Message, state: FSMContext):
    data = await state.get_data()
    await update_homework(
        data['school_id'],
        data['class_name'],
        data['subject'],
        message.text
    )
    await message.answer("Домашнее задание сохранено!", reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(Command("get_hw"))
async def get_hw_command(message: Message, state: FSMContext):
    await message.answer("Введите номер школы:", reply_markup=cancel_keyboard())
    await state.set_state(HomeworkStates.GETTING_SCHOOL)


@router.message(HomeworkStates.GETTING_SCHOOL, F.text.regexp(r'^\d+$'))
async def get_school(message: Message, state: FSMContext):
    await state.update_data(school_id=int(message.text))
    await message.answer("Введите класс (например, 10A):", reply_markup=cancel_keyboard())
    await state.set_state(HomeworkStates.GETTING_CLASS)


@router.message(HomeworkStates.GETTING_CLASS)
async def get_class(message: Message, state: FSMContext):
    await state.update_data(class_name=message.text.upper())
    await message.answer("Введите предмет:", reply_markup=subject_keyboard())
    await state.set_state(HomeworkStates.GETTING_SUBJECT)


@router.message(HomeworkStates.GETTING_SUBJECT, F.text)
async def get_subject(message: Message, state: FSMContext):
    await state.update_data(subject=message.text)
    data = await state.get_data()
    homework = await get_homework(
        school_id=data['school_id'],
        class_name=data['class_name'],
        subject=data['subject'],
    )
    if homework:
        await message.answer(f"Домашнее задание: {homework}", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Домашнее задание не найдено.", reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(F.text == "❌ Отмена",
                F.state.in_((HomeworkStates.AWAITING_SCHOOL, HomeworkStates.AWAITING_CLASS, HomeworkStates.AWAITING_SUBJECT, HomeworkStates.AWAITING_TEXT,
                            HomeworkStates.GETTING_SCHOOL, HomeworkStates.GETTING_CLASS, HomeworkStates.GETTING_SUBJECT))
                )
async def cancel_handler(message: Message, state: FSMContext):
    """
    Обработчик для кнопки отмены.
    Возвращает пользователя на предыдущий шаг, очищает данные текущего шага.
    """
    current_state = await state.get_state()
    if current_state == HomeworkStates.AWAITING_SCHOOL:
        await message.answer("Действие отменено. Введите номер школы:", reply_markup=cancel_keyboard())
        await state.set_state(HomeworkStates.AWAITING_SCHOOL)
    elif current_state == HomeworkStates.AWAITING_CLASS:
        await message.answer("Действие отменено. Введите номер школы:", reply_markup=cancel_keyboard())
        await state.set_state(HomeworkStates.AWAITING_SCHOOL)
    elif current_state == HomeworkStates.AWAITING_SUBJECT:
        await message.answer("Действие отменено. Введите класс:", reply_markup=cancel_keyboard())
        await state.set_state(HomeworkStates.AWAITING_CLASS)
    elif current_state == HomeworkStates.AWAITING_TEXT:
        await message.answer("Действие отменено. Введите предмет:", reply_markup=cancel_keyboard())
        await state.set_state(HomeworkStates.AWAITING_SUBJECT)
    elif current_state == HomeworkStates.GETTING_SCHOOL:
        await message.answer("Действие отменено. Введите номер школы:", reply_markup=cancel_keyboard())
        await state.set_state(HomeworkStates.GETTING_SCHOOL)
    elif current_state == HomeworkStates.GETTING_CLASS:
        await message.answer("Действие отменено. Введите номер школы:", reply_markup=cancel_keyboard())
        await state.set_state(HomeworkStates.GETTING_SCHOOL)
    elif current_state == HomeworkStates.GETTING_SUBJECT:
        await message.answer("Действие отменено. Введите класс:", reply_markup=cancel_keyboard())
        await state.set_state(HomeworkStates.GETTING_CLASS)
    else:
        await message.answer("Действие отменено.", reply_markup=ReplyKeyboardRemove())
    await state.clear()