import asyncio
import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

from Request_collection import Request_collection
from Request import Request

all_user_reqs = {'curr': Request_collection()}
all_user_reqs['curr'].generate_random_requests(num=random.randint(10, 30))
# t.me/TestBotHelloWorld_bot

with open('.env', 'r') as file:
    token = file.readline().strip().split('=')[1]

API_TOKEN = token

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
bot['api_timeout'] = 10000  # Установка тайм-аута в 100 секунд


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard_menu = InlineKeyboardMarkup(row_width=2)
    keyboard_menu.add(
        InlineKeyboardButton("Запросить оборудование", callback_data='create_request'),
        InlineKeyboardButton("Мои запросы", callback_data='show_requests'),
        InlineKeyboardButton("Сменить пользователя", callback_data='change_user'),
    )
    all_reqs_message = 'Вы успешно авторизованы!'
    await message.answer(all_reqs_message, reply_markup=keyboard_menu)


# группа методов ветки просмотра созданных запросов - первая версия
@dp.callback_query_handler(lambda c: c.data == 'show_requests')
async def process_callback_button_click(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    keyboard_menu = InlineKeyboardMarkup(row_width=1)
    keyboard_menu.add(
        InlineKeyboardButton("Ожидающие выдачи", callback_data='show_awaiting'),
        InlineKeyboardButton("В доставке", callback_data='show_approved'),
        InlineKeyboardButton("Обрабатываются", callback_data='show_processing'),
        InlineKeyboardButton("Отказано", callback_data='show_declined')
    )
    all_reqs_message = 'На данный момент у вас имеется ' + str(
        len(all_user_reqs['curr'])) + ' запросов, где:\n' + \
                       str(len(all_user_reqs['curr'].get_ready_requests_id())) + ' ожидающих получения,\n' + \
                       str(len(all_user_reqs['curr'].get_approved_requests_id())) + ' в доставке,\n' + \
                       str(len(all_user_reqs['curr'].get_awaiting_requests_id())) + ' в обработке,\n' + \
                       str(len(all_user_reqs['curr'].get_declined_requests_id())) + ' отклонены'
    await bot.send_message(callback_query.from_user.id, all_reqs_message, reply_markup=keyboard_menu)
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


# Просмотр готового к получению оборудования

back_to_show_all_reqs = InlineKeyboardMarkup()
back_to_show_all_reqs.add(InlineKeyboardButton("Назад", callback_data='show_requests'))


@dp.callback_query_handler(lambda c: c.data == 'show_awaiting')
async def process_callback_button_click(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    reqs = all_user_reqs["curr"].get_ready_requests()
    mess = f'на данный момент {len(reqs)} запрос(ов) ожидают выдачи:\n'
    # for i in all_user_reqs['curr'].get_awaiting_requests():
    #    mess += '\n-----------------------------------------------------------------------------------------------------\n\n'
    #    mess += f'ID = {i.id}\n\nОборудование: {i.equipment}\n\nКоличество: {i.number}\n\nПостамат: {i.postamat_id}\n'
    # mess += '\n-----------------------------------------------------------------------------------------------------\n\n'
    # mess += 'Для забора оборудования приложите пропуск ВШЭ к считывателю указанного постамата'
    keyboard = gen_reqs_keyboard(reqs, 'show_requests')
    await bot.send_message(callback_query.from_user.id, mess, reply_markup=keyboard)
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


# Просмотр одобренных запросов, которые еще в доставке
@dp.callback_query_handler(lambda c: c.data == 'show_approved')
async def process_callback_button_click(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    reqs = all_user_reqs["curr"].get_approved_requests()
    mess = f'на данный момент {len(all_user_reqs["curr"].get_awaiting_requests())} запрос(ов) находятся в доставке:\n'
    keyboard = gen_reqs_keyboard(reqs, 'show_requests')
    await bot.send_message(callback_query.from_user.id, mess, reply_markup=keyboard)
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


# Просмотр одобренных запросов, которые в обработке
@dp.callback_query_handler(lambda c: c.data == 'show_processing')
async def process_callback_button_click(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    reqs = all_user_reqs["curr"].get_awaiting_requests()
    mess = f'на данный момент {len(reqs)} запрос(ов) находятся в обработке:\n'
    keyboard = gen_reqs_keyboard(reqs, 'show_requests')
    await bot.send_message(callback_query.from_user.id, mess, reply_markup=keyboard)
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


# Просмотр одобренных запросов, в которых отказано
@dp.callback_query_handler(lambda c: c.data == 'show_declined')
async def process_callback_button_click(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    reqs = all_user_reqs["curr"].get_declined_requests()
    mess = f'на данный момент {len(reqs)} ваших запрос(ов) отклонены:\n'
    keyboard = gen_reqs_keyboard(reqs, 'show_requests')
    await bot.send_message(callback_query.from_user.id, mess, reply_markup=keyboard)
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


def gen_reqs_keyboard(reqs_list, back_name):
    new_keyboard = InlineKeyboardMarkup()
    for i in reqs_list:
        new_keyboard.add(InlineKeyboardButton(f'ID: {i.id}\n{i.equipment}, {i.number} шт, Постамат: {i.postamat_id}',
                                              callback_data='show_requests'))
    new_keyboard.add(InlineKeyboardButton("Назад", callback_data=back_name))
    return new_keyboard


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    # здесь должен делаться запрос к бд и оттуда в all_user_reqs вытягиваться в all_user_reqs[userid по телеге/еще как хз] данные по запросам пользователя,
    # all_user_reqs[userid по телеге/еще как хз] это класс Request_collection
