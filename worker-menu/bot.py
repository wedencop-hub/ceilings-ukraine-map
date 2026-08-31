import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

bot = Bot(TOKEN)
dp = Dispatcher()


def menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🗺 Мои объекты", url="https://t.me/CeilingsUkraineMapBot"),
                InlineKeyboardButton(text="💰 Прайс", url="https://t.me/ceiling_price_ua_bot"),
            ],
            [
                InlineKeyboardButton(text="📦 Комплектация", callback_data="coming_soon"),
                InlineKeyboardButton(text="📋 Регламент", callback_data="coming_soon"),
            ],
            [
                InlineKeyboardButton(text="📸 Сдать отчёт", callback_data="coming_soon"),
                InlineKeyboardButton(text="🆘 Помощь", callback_data="coming_soon"),
            ],
        ]
    )


def menu_text(message: types.Message) -> str:
    name = message.from_user.first_name if message.from_user else "коллега"
    return (
        f"👋 <b>Добро пожаловать, {name}!</b>\n\n"
        "Твой рабочий кабинет монтажника.\n\n"
        "Выбери, что нужно сделать:"
    )


async def send_menu(message: types.Message):
    await message.answer(menu_text(message), reply_markup=menu_keyboard(), parse_mode="HTML")


@dp.message(Command("start"))
async def start(message: types.Message):
    await send_menu(message)


@dp.message(Command("menu"))
async def menu(message: types.Message):
    await send_menu(message)


@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "coming_soon":
        await callback.answer("Раздел будет добавлен позже", show_alert=True)
    else:
        await callback.answer()


async def main():
    await bot.set_my_commands([
        BotCommand(command="start", description="Открыть кабинет монтажника"),
        BotCommand(command="menu", description="Показать рабочее меню"),
    ])
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
