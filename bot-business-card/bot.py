"""
Бот-визитка автосервиса TurboFix
Демонстрационный проект для портфолио.
Запуск: pip install aiogram && python bot.py
"""
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ЗАМЕНИТЕ НА ВАШИ ДАННЫЕ
BOT_TOKEN = "YOUR_TOKEN_HERE"
ADMIN_ID = 123456789  # Ваш Telegram ID для уведомлений

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

INFO = {
    "greeting": (
        "🔧 <b>TurboFix — автосервис №1</b>\n\n"
        "Ремонт и обслуживание любых марок авто.\n"
        "Гарантия на все работы — 12 месяцев.\n"
        "Бесплатная диагностика при ремонте!"
    ),
    "services": (
        "🔧 <b>Наши услуги:</b>\n\n"
        "🛢 Замена масла — от 500 ₽\n"
        "🔩 Диагностика — БЕСПЛАТНО\n"
        "⚙️ Ремонт двигателя — от 15 000 ₽\n"
        "🛞 Шиномонтаж — от 1 500 ₽\n"
        "❄️ Заправка кондиционера — от 2 000 ₽"
    ),
    "contacts": (
        "📍 г. Екатеринбург, ул. Механическая, 42\n"
        "🕐 Пн–Сб: 9:00–20:00, Вс: выходной\n"
        "📞 +7 (343) 999-88-77\n"
        "🅿️ Бесплатная парковка"
    ),
}

def main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔧 Услуги и цены", callback_data="services")],
        [InlineKeyboardButton(text="📍 Как добраться", callback_data="contacts")],
        [InlineKeyboardButton(text="📞 Записаться на ремонт", callback_data="book")],
    ])

def back_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Главное меню", callback_data="main")]
    ])

@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer(INFO["greeting"], parse_mode="HTML", reply_markup=main_kb())

@dp.callback_query(F.data == "main")
async def to_main(c: types.CallbackQuery):
    await c.message.edit_text(INFO["greeting"], parse_mode="HTML", reply_markup=main_kb())

@dp.callback_query(F.data == "services")
async def services(c: types.CallbackQuery):
    await c.message.edit_text(INFO["services"], parse_mode="HTML", reply_markup=back_kb())

@dp.callback_query(F.data == "contacts")
async def contacts(c: types.CallbackQuery):
    await c.message.edit_text(INFO["contacts"], parse_mode="HTML", reply_markup=back_kb())

@dp.callback_query(F.data == "book")
async def book(c: types.CallbackQuery):
    await c.message.edit_text(
        "📞 <b>Запись на ремонт:</b>\n\nПозвоните нам или напишите — подберём удобное время!",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📞 Позвонить", url="tel:+73439998877")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="main")],
        ])
    )
    await bot.send_message(ADMIN_ID, f"🔔 @{c.from_user.username} хочет записаться на ремонт")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
