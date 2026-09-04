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

MAP_BOT = "https://t.me/CeilingsUkraineMapBot"
PRICE_BOT = "https://t.me/ceiling_price_ua_bot"


def menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🗺 КАРТА МОНТАЖНИКА", url=f"{MAP_BOT}?profile")],
            [InlineKeyboardButton(text="📤 ПОДІЛИТИСЯ З КОЛЕГАМИ", switch_inline_query="🗺 Карта монтажника")],
            [InlineKeyboardButton(text="💰 ПРАЙС МОНТАЖНИКА", url=f"{PRICE_BOT}?profile")],
            [InlineKeyboardButton(text="📤 ПОДІЛИТИСЯ З КОЛЕГАМИ", switch_inline_query="💰 Прайс монтажника")],
        ]
    )


def menu_text(message: types.Message) -> str:
    name = message.from_user.first_name if message.from_user else "колего"
    return (
        f"👋 <b>КАБІНЕТ МОНТАЖНИКА</b>\n\n"
        f"Вітаємо, {name}!\n\n"
        "Тут зібрані два корисні інструменти для монтажників.\n\n"
        "🗺 <b>КАРТА МОНТАЖНИКА</b>\n"
        "Виробництва, постачальники, заправки газом, магазини, склади та інші корисні локації.\n"
        "Якщо потрібної точки немає — її можна <b>запропонувати додати</b>.\n\n"
        "💰 <b>ПРАЙС МОНТАЖНИКА</b>\n"
        "Вкажіть свою ціну та побачте середню ціну по ринку.\n"
        "Якщо потрібної позиції немає — її можна <b>запропонувати додати</b>.\n\n"
        "🤝 Разом створюємо корисні інструменти для монтажників по всій Україні."
    )


async def send_menu(message: types.Message):
    await message.answer(menu_text(message), reply_markup=menu_keyboard(), parse_mode="HTML")


@dp.message(Command("start"))
async def start(message: types.Message):
    await send_menu(message)


@dp.message(Command("menu"))
async def menu(message: types.Message):
    await send_menu(message)


async def main():
    await bot.set_my_commands([
        BotCommand(command="start", description="Відкрити кабінет монтажника"),
        BotCommand(command="menu", description="Показати робоче меню"),
    ])
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
