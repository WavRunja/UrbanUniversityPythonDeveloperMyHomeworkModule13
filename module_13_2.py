import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types

# Выполните все необходимые действия, создав и подготовив Telegram-бот для дальнейших заданий:
api = "Specify_your_API_token,_which_you_received_from_BotFather_in_Telegram"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


# К коду из подготовительного видео напишите две асинхронные функции:
# 1. start(message) - печатает строку в консоли 'Привет! Я бот помогающий твоему здоровью.'.
# Запускается только когда написана команда '/start' в чате с ботом. (используйте соответствующий декоратор)
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    print("Привет! Я бот помогающий твоему здоровью.")


# 2. all_massages(message) - печатает строку в консоли 'Введите команду /start, чтобы начать общение.'.
# Запускается при любом обращении не описанном ранее. (используйте соответствующий декоратор)
@dp.message_handler()
async def all_messages(message: types.Message):
    print("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
