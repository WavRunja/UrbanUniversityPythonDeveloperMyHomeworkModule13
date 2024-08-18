# module_13_3.py

# Домашнее задание по теме "Методы отправки сообщений".

# Задача "Он мне ответил!".
# Измените функции start и all_messages так, чтобы вместо вывода в консоль строки отправлялись в чате телеграм.
# Запустите ваш Telegram-бот и проверьте его на работоспособность.

import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types

api = "Specify_your_API_token,_which_you_received_from_BotFather_in_Telegram"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # print("Привет! Я бот помогающий твоему здоровью.")
    await message.answer("Привет! Я бот помогающий твоему здоровью.")


@dp.message_handler()
async def all_messages(message: types.Message):
    # print("Введите команду /start, чтобы начать общение.")
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
