import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(MENU_TEXT, reply_markup=menu_keyboard(), parse_mode="HTML")


@dp.message(Command("menu"))
async def menu(message: types.Message):
    await message.answer(MENU_TEXT, reply_markup=menu_keyboard(), parse_mode="HTML")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
