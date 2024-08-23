# module_13_6.py

# Домашнее задание по теме "Инлайн клавиатуры".

# Задача "Ещё больше выбора".
# Необходимо дополнить код предыдущей задачи, чтобы при нажатии на кнопку 'Рассчитать' присылалась Inline-клавиатруа.
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

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
    # Клавиатура с двумя кнопками
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Рассчитать"), KeyboardButton("Информация"))

    await message.answer(
        "Привет! Я бот, помогающий твоему здоровью.\nНажмите 'Рассчитать', чтобы начать расчет нормы калорий.",
        reply_markup=keyboard
    )


# Кнопка "Рассчитать"
@dp.message_handler(lambda message: message.text.lower() == 'рассчитать')
async def main_menu(message: types.Message):
    # Создайте клавиатуру InlineKeyboardMarkup с 2 кнопками InlineKeyboardButton:
    inline_kb = InlineKeyboardMarkup(row_width=1)
    # С текстом 'Рассчитать норму калорий' и callback_data='calories'
    # С текстом 'Формулы расчёта' и callback_data='formulas'
    inline_kb.add(InlineKeyboardButton("Рассчитать норму калорий", callback_data='calories'),
                  InlineKeyboardButton("Формулы расчёта", callback_data='formulas'))

    # Сообщение с Inline-клавиатурой
    await message.answer("Выберите опцию:", reply_markup=inline_kb)


# Для кнопки "Формулы расчёта"
@dp.callback_query_handler(lambda call: call.data == 'formulas')
async def get_formulas(call: types.CallbackQuery):
    formula_message = ("Формула Миффлина-Сан Жеора:\n"
                       "Для мужчин: 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) + 5\n"
                       "Для женщин: 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) - 161")
    await call.message.answer(formula_message)


# Для кнопки "Рассчитать норму калорий"
@dp.callback_query_handler(lambda call: call.data == 'calories')
async def set_age(call: types.CallbackQuery):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()


# Ввод возраста
@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer("Введите свой рост (в см):")
    await UserState.growth.set()


# Ввод роста
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

# По итогу получится следующий алгоритм:
# 1. Вводится команда /start
# 2. На эту команду присылается обычное меню: 'Рассчитать' и 'Информация'.
# 3. В ответ на кнопку 'Рассчитать' присылается Inline меню: 'Рассчитать норму калорий' и 'Формулы расчёта'
# 4. По Inline кнопке 'Формулы расчёта' присылается сообщение с формулой.
# 5. По Inline кнопке 'Рассчитать норму калорий' начинает работать машина состояний по цепочке.
