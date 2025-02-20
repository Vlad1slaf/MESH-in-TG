from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from services.logger import logger

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    logger.info(f"User {message.from_user.id} started bot")
    await message.answer(
        "📚 Добро пожаловать в бота для домашних заданий!\n"
        "Используйте /help для списка команд"
    )


@router.message(Command("help"))
async def help_handler(message: Message):
    help_text = (
        "🔍 Доступные команды:\n"
        "/start - Начало работы\n"
        "/login - Авторизация\n"
        "/add_hw - Добавление дз(функция для учителей)\n"
        "/get_hw - Получение дз(функция для учеников)\n"
        "/help - Справка"
    )
    await message.answer(help_text)
