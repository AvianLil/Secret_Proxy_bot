import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web

# ТОКЕН (убедись, что он верный)
TOKEN = "8523176868:AAHmV_fqwqLuVrUY5bvU8c_NxgKDwikLvM"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Данные для бота
SERVER_IPS = {
    "funtime": ["ft-proxy.net:25565", "play.funtime.su"],
    "holyworld": ["holy-proxy.ru:25565"],
    "reallyworld": ["rw-proxy.com:25565"]
}

# Кнопка "Назад" для переиспользования
def back_button():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="main_menu"))
    return builder.as_markup()

# Главное меню
def main_kb():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🍴 Купить прокси", callback_data="buy"))
    builder.row(
        types.InlineKeyboardButton(text="🎮 Профиль", callback_data="profile"),
        types.InlineKeyboardButton(text="🔮 Поддержка", url="https://t.me/твой_ник")
    )
    builder.row(
        types.InlineKeyboardButton(text="🔵 Подписка", callback_data="sub"),
        types.InlineKeyboardButton(text="🧬 Конструктор", callback_data="build")
    )
    return builder.as_markup()

# Обработчик команды /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("👋 Добро пожаловать в FlugerProxy!\n\nВыбери нужный раздел ниже:", 
                         reply_markup=main_kb(), parse_mode="Markdown")

# Возврат в главное меню (редактирование старого сообщения)
@dp.callback_query(F.data == "main_menu")
async def back_to_main(call: types.CallbackQuery):
    await call.message.edit_text("👋 Добро пожаловать в FlugerProxy!\n\nВыбери нужный раздел ниже:", 
                                 reply_markup=main_kb(), parse_mode="Markdown")
    await call.answer()

# Раздел ПРОФИЛЬ (заменяет старое сообщение)
@dp.callback_query(F.data == "profile")
async def show_profile(call: types.CallbackQuery):
    text = (f"👤 Ваш профиль\n\n"
            f"🆔 ID: {call.from_user.id}\n"
            f"💰 Баланс: 0.00 ₽\n"
            f"💎 Статус: Бесплатный")
    await call.message.edit_text(text, reply_markup=back_button(), parse_mode="Markdown")
    await call.answer()

# Раздел ВЫБОР СЕРВЕРА
@dp.callback_query(F.data == "buy")
async def choose_server(call: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="⚔️ FunTime", callback_data="get_ft"))
    builder.row(types.InlineKeyboardButton(text="🌟 HolyWorld", callback_data="get_hw"))
    builder.row(types.InlineKeyboardButton(text="💎 ReallyWorld", callback_data="get_rw"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu"))
    
    await call.message.edit_text("🎯 Выбери сервер для прокси:", 
                                 reply_markup=builder.as_markup(), parse_mode="Markdown")
    await call.answer()

# Выдача прокси (новым сообщением, чтобы его можно было скопировать)
@dp.callback_query(F.data.startswith("get_"))
async def send_proxy(call: types.CallbackQuery):
    srv_code = call.data.split("_")[1]
    srv_name = {"ft": "funtime", "hw": "holyworld", "rw": "reallyworld"}.get(srv_code)
    proxy = random.choice(SERVER_IPS[srv_name])
    
    await call.message.answer(f"🚀 Твой прокси для {srv_name.upper()}:\n\n{proxy}\n\n_Нажми на IP, чтобы скопировать_", 
                              parse_mode="Markdown", reply_markup=back_button())
    await call.answer()

# Заглушки для красоты
@dp.callback_query(F.data.in_({"sub", "build"}))
async def coming_soon(call: types.CallbackQuery):
    await call.message.edit_text("🚧 Этот раздел находится в разработке", 
                                 reply_markup=back_button(), parse_mode="Markdown")
    await call.answer()

# Настройка сервера для Render
async def handle(request):
    return web.Response(text="Bot is running")

async def main():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await asyncio.gather(site.start(), dp.start_polling(bot))

if name == "main":
    asyncio.run(main())
