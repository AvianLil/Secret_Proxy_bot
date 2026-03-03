import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Вставь свой токен от @BotFather ниже
TOKEN = "8523176868:AAHmv_fqwqqLuVrUY5bvU8c_NxgKDWikLvM"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Главное меню как на скриншоте
def main_menu():
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
    await message.answer_photo(
        photo="https://i.imgur.com/8nNnNnN.jpg", # Замени на свою картинку
        caption="👋 Привет! Добро пожаловать в FlugerProxy.\n\nОплачивая подписку, ты получаешь доступ к конструктору - генерируй бесконечное количество прокси.",
        reply_markup=main_menu()
    )

@dp.callback_query(F.data == "profile")
async def profile(call: types.CallbackQuery):
    await call.message.edit_caption(
        caption=f"✨ Профиль\n\nЮзер: @{call.from_user.username}\nБаланс: 0.00 ₽\n\nПодписка: нет подписки",
        reply_markup=main_menu() # Здесь можно добавить кнопки из твоего второго скрина
    )

async def main():
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())
