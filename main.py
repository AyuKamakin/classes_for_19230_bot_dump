import asyncio
import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

from Request_collection import Request_collection
from Request import Request

all_user_reqs = {'curr': Request_collection()}
all_user_reqs['curr'].generate_random_requests(num=100)
# t.me/TestBotHelloWorld_bot

with open('.env', 'r') as file:
    token = file.readline().strip().split('=')[1]

API_TOKEN = token

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
bot['api_timeout'] = 100  # Установка тайм-аута в 100 секунд


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard_menu = InlineKeyboardMarkup(row_width=2)
    keyboard_menu.add(
        InlineKeyboardButton("Ожидающие выдачи", callback_data='awaiting'),
        InlineKeyboardButton("Одобренные", callback_data='approved'),
        InlineKeyboardButton("В обработке", callback_data='processing'),
        InlineKeyboardButton("Отказано", callback_data='declined')
    )
    all_reqs_message = 'Вы успешно авторизованы!\nНа данный момент у вас имеется ' + str(len(all_user_reqs['curr'])) + ' запросов, где:\n' + \
               str(len(all_user_reqs['curr'].get_ready_requests_id())) + ' ожидающих получения,\n' + \
               str(len(all_user_reqs['curr'].get_approved_requests_id())) + ' одобренных,\n' + \
               str(len(all_user_reqs['curr'].get_awaiting_requests_id())) + ' в обработке,\n' + \
               str(len(all_user_reqs['curr'].get_declined_requests_id())) + ' отклонены'
    await message.answer(all_reqs_message, reply_markup=keyboard_menu)


# Обработчик Inline кнопки
@dp.callback_query_handler(lambda c: c.data == 'button_click1')
async def process_callback_button_click(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Вы нажали на Inline кнопку цифры 1.")


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
