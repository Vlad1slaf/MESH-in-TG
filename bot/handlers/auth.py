from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config.settings import settings
import aiohttp
import urllib.parse
from services.database import save_yandex_token
from typing import Union
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
import logging  # Импортируем модуль logging


logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

router = Router()


class AuthState(StatesGroup):
    WAITING_FOR_CODE = State()


@router.message(Command("login"))
async def cmd_start(message: Message, bot: Bot, state: FSMContext):
    """Отправляет пользователю ссылку для авторизации."""
    auth_url = (
        f"https://oauth.yandex.ru/authorize?"
        f"response_type=code&client_id={settings.YANDEX_CLIENT_ID}&redirect_uri={settings.REDIRECT_URI}"
    )
    keyboard = [
        [InlineKeyboardButton(text="🔑 Авторизация через Яндекс", url=auth_url)],
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await message.answer(
        "Для доступа к функциям учителя требуется авторизация:\n\n"
        "Нажмите на кнопку ниже, чтобы авторизоваться через Яндекс.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    await state.set_state(AuthState.WAITING_FOR_CODE)
    logger.info(f"User {message.from_user.id} запросил авторизацию.")


@router.message(AuthState.WAITING_FOR_CODE, F.text)
async def process_code(message: Message, bot: Bot, state: FSMContext):
    """
    Обрабатывает полученный код авторизации и обменивает его на access token.
    """
    full_url = message.text.strip() # Получаем полную ссылку
    logger.debug(f"Получена полная ссылка от пользователя {message.from_user.id}: {full_url}")

    try:
        parsed_url = urllib.parse.urlparse(full_url)
        code = urllib.parse.parse_qs(parsed_url.query)['code'][0] # Извлекаем code из URL
        logger.debug(f"Извлечен code авторизации: {code}")
    except KeyError:
        await message.answer("Не удалось извлечь код авторизации из URL.")
        await state.clear()
        return

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": settings.YANDEX_CLIENT_ID,
        "client_secret": settings.YANDEX_CLIENT_SECRET.get_secret_value(),  #  Получаем значение из SecretStr
        "redirect_uri": settings.REDIRECT_URI,
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                "https://oauth.yandex.ru/token", data=data
            ) as response:
                response.raise_for_status()
                token_data = await response.json()
                access_token = token_data["access_token"]
                logger.info(
                    f"Успешно получен access token для пользователя {message.from_user.id}."
                )

                # Сохраняем токен в базу данных
                user_id = message.from_user.id
                await save_yandex_token(user_id, access_token)
                logger.info(
                    f"Access token для пользователя {message.from_user.id} сохранен в БД."
                )

                await message.answer(
                    "Авторизация прошла успешно!\n"
                    "Теперь вы можете использовать функции бота.",
                    reply_markup=ReplyKeyboardRemove(),
                )
                await state.clear()  # Сбрасываем состояние
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка при обмене code на token: {e}")
            await message.answer(
                "Произошла ошибка при обмене code на token.\n"
                "Попробуйте еще раз.",
                reply_markup=ReplyKeyboardRemove(),
            )
            await state.clear()
        except Exception as e:
            logger.exception(f"Неизвестная ошибка: {e}")
            await message.answer(
                "Произошла неизвестная ошибка.\n" "Попробуйте еще раз.",
                reply_markup=ReplyKeyboardRemove(),
            )
            await state.clear()