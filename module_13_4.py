# module_13_4.py

# Задача "Цепочка вопросов":
# Необходимо сделать цепочку обработки состояний для нахождения нормы калорий для человека.

# Группа состояний:
# 1. Импортируйте классы State и StateGroup из aiogram.dispatcher.filters.state.
# import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

api = "Specify_your_API_token,_which_you_received_from_BotFather_in_Telegram"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


# 2. Создайте класс UserState наследованный от StateGroup.
class UserState(StatesGroup):
    # 3. Внутри этого класса опишите 3 объекта класса State: age, growth, weight (возраст, рост, вес).
    age = State()
    growth = State()
    weight = State()
    male = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "Привет! Я бот, помогающий твоему здоровью.\nВведите 'Calories', чтобы рассчитать норму калорий.")


# Оберните функцию set_age(message) в message_handler, который реагирует на текстовое сообщение 'Calories'.
@dp.message_handler(lambda message: message.text.lower() == 'calories')
# Напишите следующие функции для обработки состояний:
# Функцию set_age(message):
async def set_age(message: types.Message):
    # Эта функция должна выводить в Telegram-бот сообщение 'Введите свой возраст:'.
    await message.answer("Введите свой возраст:")
    # После ожидать ввода возраста в атрибут UserState.age при помощи метода set.
    await UserState.age.set()


# Оберните функцию set_growth(message, state) в message_handler,
# который реагирует на переданное состояние UserState.age.
@dp.message_handler(state=UserState.age)
# Функцию set_growth(message, state):
async def set_growth(message: types.Message, state: FSMContext):
    # Эта функция должна обновлять данные в состоянии age на
    # message.text (написанное пользователем сообщение). Используйте метод update_data.
    await state.update_data(age=int(message.text))
    # Далее должна выводить в Telegram-бот сообщение 'Введите свой рост:'.
    await message.answer("Введите свой рост (в см):")
    # После ожидать ввода роста в атрибут UserState.growth при помощи метода set.
    await UserState.growth.set()


# Оберните её в message_handler, который реагирует на переданное состояние UserState.growth.
@dp.message_handler(state=UserState.growth)
# Функцию set_weight(message, state):
async def set_weight(message: types.Message, state: FSMContext):
    # Эта функция должна обновлять данные в состоянии growth на message.text (написанное пользователем сообщение).
    # Используйте метод update_data.
    await state.update_data(growth=int(message.text))
    # Далее должна выводить в Telegram-бот сообщение 'Введите свой вес:'.
    await message.answer("Введите свой вес (в кг):")
    # После ожидать ввода роста в атрибут UserState.weight при помощи метода set.
    await UserState.weight.set()


# Оберните её в message_handler, который реагирует на переданное состояние UserState.weight.
@dp.message_handler(state=UserState.weight)
# Функцию send_calories(message, state):
async def send_calories(message: types.Message, state: FSMContext):
    # Эта функция должна обновлять данные в состоянии weight на message.text (написанное пользователем сообщение).
    # Используйте метод update_data.
    await state.update_data(weight=int(message.text))
    # Далее должна выводить в Telegram-бот сообщение 'Укажите свой пол: М или Ж'.
    await message.answer("Укажите свой пол: М или Ж")
    # После ожидать ввода пола в атрибут UserState.male при помощи метода set.
    await UserState.male.set()


@dp.message_handler(state=UserState.male)
# Функцию set_male(message, state):
async def set_male(message: types.Message, state: FSMContext):
    # Эта функция должна обновлять данные в состоянии male на
    # message.text (написанное пользователем сообщение). Используйте метод update_data.
    await state.update_data(male=message.text)

    # Далее в функции запомните в переменную data все ранее введённые состояния при помощи state.get_data().
    data = await state.get_data()
    age = data['age']
    growth = data['growth']
    weight = data['weight']
    male = data['male']

    # Используйте упрощённую формулу Миффлина - Сан Жеора для подсчёта нормы калорий
    # (для женщин или мужчин - на ваше усмотрение).
    # Данные для формулы берите из ранее объявленной переменной data по ключам age, growth и weight соответственно.
    if male == 'М':  # Условие для примера, можете заменить на выбор пола
        # Формула для мужчин
        calories = 10 * weight + 6.25 * growth - 5 * age + 5
    elif male == 'Ж':
        # Формула для женщин
        calories = 10 * weight + 6.25 * growth - 5 * age - 161

    # Результат вычисления по формуле отправьте ответом пользователю в Telegram-бот.
    await message.answer(f"Ваша норма калорий: {calories:.2f} ккал в сутки.")

    # Финишируйте машину состояний методом finish().
    await state.finish()


@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
