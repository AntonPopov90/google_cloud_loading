"""1. Приветствие(какие действия)
    2. Отдельно кнопки
   3. Админка?
   4. Отделить спам(общение только кнопками)
   5. не загружается сразу на сервер(create_and_upload_file не работает
   )"""
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from main import insert_permission, create_and_upload_file

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

API_TOKEN: str = os.getenv('TOKEN')
OWNER_ID: str = os.getenv('OWNER_ID')
OWNER_EMAIL: str = os.getenv('OWNER_EMAIL')
logging.basicConfig(level=logging.INFO)

bot = Bot(API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

button1 = KeyboardButton('Да')
button2 = KeyboardButton('Нет')
markup = ReplyKeyboardMarkup().row(
    button1, button2)


class UserState(StatesGroup):
    name = State()
    email = State()


@dp.message_handler(commands=['start'])
async def user_register(message: types.Message):
    await message.answer('Введите ваше имя')
    await UserState.name.set()


@dp.message_handler(state=UserState.name)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Отлично! Теперь введите ваш email.")
    await UserState.next()


@dp.message_handler(state=UserState.email)
async def get_address(message: types.Message, state: FSMContext):
    if "@" in message.text:
        await state.update_data(address=message.text)
        data = await state.get_data()
        await bot.send_message(OWNER_ID, f"Запрос на доступ от\n"
                                         f"Имя: {data['username']}\n"
                                         f"email: {data['address']}", reply_markup=markup)

        @dp.message_handler(lambda message: message.text == "Да")
        async def give_access(message: types.Message):
            await message.reply("Отправка прав доступа", reply_markup=types.ReplyKeyboardRemove())
            insert_permission(data['address'])

        @dp.message_handler(lambda message: message.text == "Нет")
        async def deny_access(message: types.Message):
            await message.reply('отказ в доступе', reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer('Некорректный email')
    await state.finish()


@dp.callback_query_handler(text='user_id')
async def user_id_inline_callback(callback_query: types.CallbackQuery):
    await callback_query.answer(f"Ваш ID: {callback_query.from_user.id}", True)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
