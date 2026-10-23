import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
dp = Dispatcher()

HELP = (
    "Пришли 4 числа через пробел:\n"
    "закупка продажа доставка тонны\n\n"
    "Пример: 12800 14200 650 60"
)


def verdict(profit_per_t, margin):
    if profit_per_t <= 0:
        return "Сделка убыточная"
    if margin < 3:
        return "Маржа маленькая, риск не окупится"
    if margin < 7:
        return "Нормальная сделка"
    return "Отличная сделка, проверь, нет ли подвоха"


def calculate(text):
    parts = text.replace(",", ".").split()
    if len(parts) != 4:
        return None
    buy, sell, delivery, tonnes = [float(x) for x in parts]
    per_t = sell - buy - delivery
    margin = per_t / sell * 100
    total = per_t * tonnes
    return (
        f"Прибыль на тонне: {per_t:,.0f} руб\n"
        f"Маржа: {margin:.1f}%\n"
        f"Прибыль по сделке: {total:,.0f} руб\n\n"
        f"Вердикт: {verdict(per_t, margin)}"
    )


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Я считаю прибыль сделки.\n\n" + HELP)


@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(HELP)


@dp.message()
async def calc(message: Message):
    try:
        result = calculate(message.text or "")
    except ValueError:
        result = None
    if result is None:
        await message.answer("Не понял формат.\n\n" + HELP)
    else:
        await message.answer(result)


async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    print("Калькулятор запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())