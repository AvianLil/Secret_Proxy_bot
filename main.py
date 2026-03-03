import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ВНИМАНИЕ: Замени цифры ниже на свой токен!
TOKEN = "8523176868:AAHmv_fqwqqLuVrUY5bvU8c_NxgKDWikLvM"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список бесплатных прокси
FREE_PROXIES = [
    "154.23.11.5:25565",
    "92.112.43.10:25565",
    "mc.hypixel.net",
    "play.mineproxies.ru:25565"
]

def main_kb():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🍴 Купить прокси", callback_data="buy"))
    builder.row(
        types.InlineKeyboardButton(text="🎮 Профиль", callback_data="profile"),
        types.InlineKeyboardButton(text="🔮 Поддержка", url="https://t.me/Artiisell")
    )
    builder.row(
        types.InlineKeyboardButton(text="🔵 Подписка на прокси", callback_data="sub"),
        types.InlineKeyboardButton(text="🧬 Конструктор прокси", callback_data="build")
    )
    return builder.as_markup()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Привет! Добро пожаловать в FlugerProxy.\n\n"
        "Оплачивая подписку, ты получаешь доступ к конструктору.",
        reply_markup=main_kb()
    )

@dp.callback_query(F.data == "buy")
async def buy_proxy(call: types.CallbackQuery):
    selected_proxy = random.choice(FREE_PROXIES)
    text = (f"✅ Прокси успешно сгенерирован!\n\n"
            f"📍 Адрес: {selected_proxy}\n"
            f"👤 Тип: Бесплатный\n\n"
            f"Вставь его в Minecraft!")
    await call.message.answer(text, parse_mode="Markdown")
    await call.answer()

@dp.callback_query(F.data == "profile")
async def profile(call: types.CallbackQuery):
    text = f"✨ Профиль\n\nЮзер: @{call.from_user.username}\nБаланс: 0.00 ₽\n\nПодписка: нет"
    await call.message.answer(text, reply_markup=main_kb())
    await call.answer()

async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if name == "main":
    asyncio.run(main())
