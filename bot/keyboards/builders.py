from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def role_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="👨🏫 Учитель")
    builder.button(text="👨🎓 Ученик")
    return builder.as_markup(resize_keyboard=True)


def cancel_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="❌ Отмена")
    return builder.as_markup(resize_keyboard=True)


def get_keyboard_with_cancel(buttons: list[str]) -> ReplyKeyboardMarkup:
    """Создает клавиатуру с заданными кнопками и кнопкой "Отмена"."""
    builder = ReplyKeyboardBuilder()
    for button_text in buttons:
        builder.button(text=button_text)
    builder.button(text="❌ Отмена")
    return builder.as_markup(resize_keyboard=True)


SUBJECTS = ["математика ", "ИКТ", "алгебра", "геометрия", "информатика", "история", "экономика", "окружающий мир",
            "природоведение", "география", "биология", "физика", "химия", "ОБЖ", "ОБЗР", "экология", "астрономия",
            "обществознание", "право", "ОРКСЭ", "ОДНРК", "русский язык", "родной русский язык", "литературное чтение",
            "литература", "английский язык", "индивидуальный проект", "экономика", "иностранный язык"
            "испанский язык", "французский язык", "немецкий язык", "художественный труд", "технология", "черчение",
            "физическая культура", "изобразительное искусство", "музыка", "мировая художественная культура"]


def subject_keyboard():
    builder = ReplyKeyboardBuilder()
    for subject in SUBJECTS:
        builder.button(text=subject)
    builder.adjust(3) # Кнопки в 3 колонки
    return builder.as_markup(resize_keyboard=True)