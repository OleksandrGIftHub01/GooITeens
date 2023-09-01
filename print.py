import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from random import randint
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

TOKEN = '6500996105:AAEPAAu_mV2_yyw83JP3SPYCk6nq8BKuWb8'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

topics = {
    'історичні': ['Історія – це дослідження людських помилок', 'Головний урок історії полягає в тому, що людство необучаемость', 'Історія вчить лише тому, що вона ніколи нічому не навчила народи'],
    'цитати про життя': ['Дія не завжди приведе до щастя, але до щастя привести може лише дія.', 'Немає різниці між песимістом, який говорить: "О, це безнадійно. Не трать сил дарма", та оптимістом, який каже: "Нічого не роби. І так все буде добре". В обох випадках нічого не стається.', 'Вершина ідеальності – в простоті.'],
    'пайтонські': ['Python - це потужна, елегантна та проста мова програмування.', 'Python дозволяє розвиватися швидше та ефективніше.', 'Python - це відмінний вибір для початківців та досвідчених програмістів.'],
    'софтові': ['Софт - це магія, яка оживляє комп\'ютери.', 'Софтові рішення полегшують наше життя та покращують робочий процес.'],
}

quote_ratings = {}

@dp.callback_query_handler()
async def get_topics_info(callback_query: types.CallbackQuery):
    print(callback_query.data)
    if callback_query.data in topics.keys():
        main_topics = randint(0, len(topics[callback_query.data])-1)
        main = topics[callback_query.data][main_topics]
        quote_ratings[main] = {'likes': 0, 'dislikes': 0}
        await bot.send_message(callback_query.message.chat.id, main, reply_markup=get_rating_keyboard())
    elif callback_query.data in quote_ratings.keys():
        if callback_query.data == 'like':
            quote_ratings[callback_query.message.text]['likes'] += 1
        elif callback_query.data == 'dislike':
            quote_ratings[callback_query.message.text]['dislikes'] += 1
        await bot.send_message(callback_query.message.chat.id, get_quote_rating(callback_query.message.text), reply_markup=get_rating_keyboard())

def get_rating_keyboard():
    keyboard = InlineKeyboardMarkup()
    like_button = InlineKeyboardButton(text='Подобається', callback_data='like')
    dislike_button = InlineKeyboardButton(text='Не подобається', callback_data='dislike')
    keyboard.row(like_button, dislike_button)
    return keyboard

def get_quote_rating(quote):
    likes = quote_ratings[quote]['likes']
    dislikes = quote_ratings[quote]['dislikes']
    rating = 'Цитата: {quote}Подобається: {likes}Не подобається: {dislikes}'
    return rating

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    motivation_choice = InlineKeyboardMarkup()
    for mot in topics:
        button = InlineKeyboardButton(text=mot, callback_data=mot)
        motivation_choice.add(button)
    await message.answer(text='Привіт, Я - бот цитатник, Обери тему для цитати:', reply_markup=motivation_choice)

if __name__ == '__main__':
    executor.start_polling(dp)