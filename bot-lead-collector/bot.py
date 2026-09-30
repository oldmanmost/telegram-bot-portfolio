"""
Бот для записи к репетитору (Сбор заявок через FSM)
Демонстрационный проект для портфолио.
Запуск: pip install aiogram && python bot.py
"""
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# ЗАМЕНИТЕ НА ВАШИ ДАННЫЕ
BOT_TOKEN = "YOUR_TOKEN_HERE"
ADMIN_ID = 123456789  # Ваш Telegram ID для получения заявок

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Машина состояний для пошагового опроса
class BookingForm(StatesGroup):
    name = State()
    grade = State()
    subject = State()
    phone = State()

@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer(
        "👋 Привет! Я бот репетитора по математике Алексея Петрова.\n\n"
        "📚 10 лет опыта, 200+ учеников, средний рост оценки на 2 балла.\n\n"
        "Хотите записаться на бесплатное пробное занятие?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Да, записаться!", callback_data="start_form")],
            [InlineKeyboardButton(text="ℹ️ Узнать подробнее", callback_data="info")],
        ])
    )

@dp.callback_query(F.data == "info")
async def info(c: types.CallbackQuery):
    await c.message.answer(
        "🎓 <b>О репетиторе:</b>\n\n"
        "• МГУ, мехмат, красный диплом\n"
        "• Подготовка к ЕГЭ (средний балл учеников — 85)\n"
        "• ОГЭ, олимпиады, школьная программа\n\n"
        "💰 Стоимость: 2 000 ₽ / 60 мин\n"
        "🎁 Первое занятие — БЕСПЛАТНО!",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Записаться", callback_data="start_form")]
        ])
    )

@dp.callback_query(F.data == "start_form")
async def start_form(c: types.CallbackQuery, state: FSMContext):
    await c.message.answer("📝 Отлично! Давайте оформим запись.\n\nКак вас зовут?")
    await state.set_state(BookingForm.name)

@dp.message(BookingForm.name)
async def get_name(msg: types.Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer(
        f"Приятно познакомиться, {msg.text}! 🎉\n\nВ каком классе вы учитесь?",
        reply_markup=ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="5–7 класс"), KeyboardButton(text="8–9 класс")],
            [KeyboardButton(text="10–11 класс"), KeyboardButton(text="Студент")],
        ], resize_keyboard=True)
    )
    await state.set_state(BookingForm.grade)

@dp.message(BookingForm.grade)
async def get_grade(msg: types.Message, state: FSMContext):
    await state.update_data(grade=msg.text)
    await msg.answer(
        "Что нужно подтянуть?",
        reply_markup=ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="ЕГЭ"), KeyboardButton(text="ОГЭ")],
            [KeyboardButton(text="Школьная программа"), KeyboardButton(text="Олимпиады")],
        ], resize_keyboard=True)
    )
    await state.set_state(BookingForm.subject)

@dp.message(BookingForm.subject)
async def get_subject(msg: types.Message, state: FSMContext):
    await state.update_data(subject=msg.text)
    await msg.answer(
        "📱 Оставьте номер телефона — Алексей свяжется с вами в течение часа!",
        reply_markup=ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="📱 Отправить контакт", request_contact=True)]
        ], resize_keyboard=True)
    )
    await state.set_state(BookingForm.phone)

@dp.message(BookingForm.phone)
async def get_phone(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    phone = msg.contact.phone_number if msg.contact else msg.text

    summary = (
        f"🔔 <b>НОВАЯ ЗАЯВКА!</b>\n\n"
        f"👤 Имя: {data['name']}\n"
        f"🎓 Класс: {data['grade']}\n"
        f"📚 Цель: {data['subject']}\n"
        f"📞 Телефон: {phone}\n"
        f"🆔 @{msg.from_user.username or 'нет'}"
    )
    await bot.send_message(ADMIN_ID, summary, parse_mode="HTML")
    await msg.answer(
        "✅ <b>Заявка отправлена!</b>\n\nАлексей свяжется с вами в течение часа.\n"
        "Спасибо за доверие! 🎓",
        parse_mode="HTML",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
