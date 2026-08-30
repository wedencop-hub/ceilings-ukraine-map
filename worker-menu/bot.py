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

MENU_TEXT = """👷 <b>КАБИНЕТ МОНТАЖНИКА</b>

Все рабочие инструменты в одном месте.

Выберите нужный раздел:"""


def menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🗺 КАРТА ОБЪЕКТОВ", url="https://t.me/CeilingsUkraineMapBot")],
            [InlineKeyboardButton(text="💰 ПРАЙС МОНТАЖНИКА", url="https://t.me/ceiling_price_ua_bot")],
        ]
    )


async def send_menu(message: types.Message):
    # In a forum group this answer stays in the same topic as the command.
    await message.answer(MENU_TEXT, reply_markup=menu_keyboard(), parse_mode="HTML")


@dp.message(Command("start"))
async def start(message: types.Message):
    await send_menu(message)


@dp.message(Command("menu"))
async def menu(message: types.Message):
    await send_menu(message)


async def main():
    await bot.set_my_commands([
        BotCommand(command="start", description="Открыть кабинет монтажника"),
        BotCommand(command="menu", description="Показать рабочее меню"),
    ])
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
