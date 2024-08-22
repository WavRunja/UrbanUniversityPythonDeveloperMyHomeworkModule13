# module_13_5.py

# Задача "Меньше текста, больше кликов"

# Необходимо дополнить код предыдущей задачи,
# чтобы вопросы о параметрах тела для расчёта калорий
# выдавались по нажатию кнопки.
# import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

api = "Specify_your_API_token,_which_you_received_from_BotFather_in_Telegram"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    male = State()


# Команда /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # Создайте клавиатуру ReplyKeyboardMarkup и
    # 2 кнопки KeyboardButton на ней со следующим текстом:
    # 'Рассчитать' и 'Информация'.
    # Сделайте так, чтобы клавиатура подстраивалась под размеры интерфейса устройства
    # при помощи параметра resize_keyboard.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Рассчитать"), KeyboardButton("Информация"))

    # Используйте ранее созданную клавиатуру в ответе функции start,
    # используя параметр reply_markup.
    await message.answer(
        "Привет! Я бот, помогающий твоему здоровью.\nНажмите 'Рассчитать', чтобы начать расчет нормы калорий.",
        reply_markup=keyboard
    )


# Кнопка "Рассчитать"
# Измените massage_handler для функции set_age.
# Теперь этот хэндлер будет реагировать на текст 'Рассчитать', а не на 'Calories'.
@dp.message_handler(lambda message: message.text.lower() == 'рассчитать')
async def set_age(message: types.Message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()


# Ввод возраста
@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer("Введите свой рост (в см):")
    await UserState.growth.set()


# Ввода роста
@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await message.answer("Введите свой вес (в кг):")
    await UserState.weight.set()


# Ввод веса
@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    await message.answer("Укажите свой пол: М или Ж")
    await UserState.male.set()


# Ввод пола и расчет калорий
@dp.message_handler(state=UserState.male)
async def set_male(message: types.Message, state: FSMContext):
    await state.update_data(male=message.text)
    data = await state.get_data()
    age = data['age']
    growth = data['growth']
    weight = data['weight']
    male = data['male']

    if male.lower() == 'м':
        calories = 10 * weight + 6.25 * growth - 5 * age + 5
    elif male.lower() == 'ж':
        calories = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.answer(f"Ваша норма калорий: {calories:.2f} ккал в сутки.")
    await state.finish()


# Для неизвестных сообщений
@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer("Введите команду /start, чтобы начать общение.")

# Запуск
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

# В итоге при команде /start у вас должна присылаться клавиатура с двумя кнопками.
# При нажатии на кнопку с надписью 'Рассчитать' срабатывает функция set_age
# с которой начинается работа машины состояний для age, growth и weight.
