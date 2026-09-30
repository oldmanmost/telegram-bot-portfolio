"""
FAQ-бот для интернет-магазина (умный поиск по ключевым словам)
Демонстрационный проект для портфолио.
Запуск: pip install aiogram && python bot.py
"""
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ЗАМЕНИТЕ НА ВАШИ ДАННЫЕ
BOT_TOKEN = "YOUR_TOKEN_HERE"
ADMIN_ID = 123456789

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# База знаний бота
FAQ = [
    {"keys": ["доставк", "доставить", "привез", "сколько ждать", "срок"],
     "q": "🚚 Как работает доставка?",
     "a": "Доставка по Москве — 1 день (300 ₽). По России — 3–7 дней (500 ₽). Бесплатно от 10 000 ₽!"},
    {"keys": ["возврат", "вернуть", "обмен", "размер не подош", "не подош"],
     "q": "🔄 Можно ли вернуть или обменять?",
     "a": "Да! 14 дней на возврат без вопросов. Обмен размера — бесплатно. Курьер заберёт сам."},
    {"keys": ["оригинал", "подлин", "настоящ", "подделк", "паль"],
     "q": "✅ Это оригиналы?",
     "a": "100% оригинал. Работаем напрямую с брендами. Есть сертификаты и гарантия."},
    {"keys": ["оплат", "заплатить", "карт", "наличн", "рассрочк"],
     "q": "💳 Как оплатить?",
     "a": "Картой онлайн, наличными курьеру, СБП. Есть рассрочка 0% на 3 месяца."},
]

def faq_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=item["q"], callback_data=f"faq_{i}")]
        for i, item in enumerate(FAQ)
    ] + [[InlineKeyboardButton(text="❓ Задать свой вопрос", callback_data="ask")]])

@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer(
        "👟 <b>SneakerShop — Справочная служба</b>\n\nВыберите частый вопрос или напишите свой:",
        parse_mode="HTML", reply_markup=faq_kb()
    )

@dp.callback_query(F.data.startswith("faq_"))
async def show_faq(c: types.CallbackQuery):
    idx = int(c.data.split("_")[1])
    item = FAQ[idx]
    await c.message.answer(f"<b>{item['q']}</b>\n\n{item['a']}", parse_mode="HTML", reply_markup=faq_kb())

@dp.callback_query(F.data == "ask")
async def ask(c: types.CallbackQuery):
    await c.message.answer("✍️ Напишите ваш вопрос — менеджер ответит в течение 15 минут!")

@dp.message(F.text)
async def smart_search(msg: types.Message):
    text = msg.text.lower()
    # Ищем совпадение по ключевым словам
    for item in FAQ:
        if any(k in text for k in item["keys"]):
            await msg.answer(f"<b>{item['q']}</b>\n\n{item['a']}", parse_mode="HTML")
            return
    
    # Если не нашли, пересылаем админу
    await bot.send_message(ADMIN_ID, f"❓ Вопрос от @{msg.from_user.username}:\n{msg.text}")
    await msg.answer("🤔 Не нашёл ответ в базе? Передал ваш вопрос менеджеру — ответит в течение 15 минут!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
