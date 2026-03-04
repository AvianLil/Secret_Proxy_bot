import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web

TOKEN = "8523176868:AAHmv_fqwqqLuVrUY5bvU8c_NxgKDWikLvM"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Ссылки на твои картинки (ЗАМЕНИ НА СВОИ)
IMG_MAIN = "https://i.imgur.com/8nNnNnN.jpg"
IMG_PROFILE = "https://i.imgur.com/your_profile_image.jpg" # Твоя картинка профиля

# База реальных прокси (формат IP:PORT:USER:PASS или просто IP:PORT)
PROXIES = {
    "funtime": ["154.23.11.5:25565", "92.112.43.10:1080"],
    "holyworld": ["185.244.11.22:8000"],
    "reallyworld": ["45.132.12.55:3128"]
}

# --- КЛАВИАТУРЫ ---
def main_kb():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🍴 Купить прокси", callback_data="buy"))
    builder.row(types.InlineKeyboardButton(text="🎮 Профиль", callback_data="profile"),
                types.InlineKeyboardButton(text="🔮 Поддержка", url="https://t.me/твой_ник"))
    builder.row(types.InlineKeyboardButton(text="🔵 Подписка", callback_data="sub"),
                types.InlineKeyboardButton(text="🧬 Конструктор", callback_data="build"))
    return builder.as_markup()

def profile_kb():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="💧 Подписка на прокси", callback_data="sub"),
                types.InlineKeyboardButton(text="Пополнить баланс", callback_data="topup"))
    builder.row(types.InlineKeyboardButton(text="Купленные прокси", callback_data="my_list"))
    builder.row(types.InlineKeyboardButton(text="Реферальная программа", callback_data="ref"))
    builder.row(types.InlineKeyboardButton(text="Применить промокод", callback_data="promo"))
    builder.row(types.InlineKeyboardButton(text="Назад", callback_data="to_main"))
    return builder.as_markup()

# --- ОБРАБОТЧИКИ ---
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer_photo(photo=IMG_MAIN, caption="👋 Добро пожаловать в FlugerProxy!\n\nВыбери раздел:", 
                               reply_markup=main_kb(), parse_mode="Markdown")

@dp.callback_query(F.data == "to_main")
async def to_main(call: types.CallbackQuery):
    await call.message.edit_media(types.InputMediaPhoto(media=IMG_MAIN, caption="👋 Главное меню:"), 
                                  reply_markup=main_kb())

@dp.callback_query(F.data == "profile")
async def show_profile(call: types.CallbackQuery):
    text = f"✨ Профиль\n\nЮзер: @{call.from_user.username}\nБаланс: 0.00 ₽\n\nПодписка: нет подписки"
    await call.message.edit_media(types.InputMediaPhoto(media=IMG_PROFILE, caption=text), 
                                  reply_markup=profile_kb())

@dp.callback_query(F.data == "buy")
async def buy_menu(call: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="⚔️ FunTime", callback_data="get:funtime"))
    builder.row(types.InlineKeyboardButton(text="🌟 HolyWorld", callback_data="get:holyworld"))
    builder.row(types.InlineKeyboardButton(text="💎 ReallyWorld", callback_data="get:reallyworld"))
    builder.row(types.InlineKeyboardButton(text="Назад", callback_data="to_main"))
    await call.message.edit_caption(caption="🎯 Выбери сервер:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("get:"))
async def give_proxy(call: types.CallbackQuery):
    srv = call.data.split(":")[1]
    proxy = random.choice(PROXIES[srv])
    # Выдаем новым сообщением, чтобы было удобно копировать на телефоне
    await call.message.answer(f"🚀 Твой прокси для {srv.upper()}:\n\n{proxy}\n\n_Нажми на IP, чтобы скопировать_")
    await call.answer()

# --- СЕРВЕР И МЕНЮ КОМАНД ---
async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="start", description="Главное меню"),
        types.BotCommand(command="profile", description="Мой профиль"),
        types.BotCommand(command="undo", description="Отмена/Назад")
    ]
    await bot.set_my_commands(commands)

async def handle(request): return web.Response(text="Bot Live")

async def main():
    await set_commands(bot)
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await asyncio.gather(site.start(), dp.start_polling(bot))

if __name__ == "__main__":
    asyncio.run(main())


