import telebot
import random
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
# эта тема помогает создать разные штуки для клавиатуры телеграма, типа тех же кнопок в дайвинчике и прочая шняга
from telebot import types

# За эту тему респект
with open('token.txt', 'r') as file:
    bot_token = file.read().strip()
bot = telebot.TeleBot(token=bot_token)

# Но сейчас я тебе покажу как это сделать ещё надёжнее
# Видишь ли, текстовый файлик может совершенно случайно быть сворован
# Поэтому будем использовать .env файл

from dotenv import load_dotenv  # Импортируем стандартную библиотеку питона (её не надо качать)
from os.path import dirname, join  # Импортируем эту шнягу, она понадобиться, чтобы всегда находить наш файл
import os  # Это тоже импортируем, понадобиться для обращения к файлу с секретами

dotenv_path = join(dirname(__file__), ".env")  # Эта строка находит наш .env файл в директории
load_dotenv(dotenv_path)  # Тут мы загружаем данные из .env файла в код

print(os.getenv("TOKEN"))  # При помощи os.getenv мы обращаемся к .env файлу безопасным способом
# ВАЖНО: как правило, .env файл должен храниться в одной директории с исполняемым кодом
print(os.getenv("TRUTH_ABOUT_RUSLAN"))  # Как видишь, мы вызываем название секрета
# А код выдаёт его значение

# Список категорий подарков
categories = {
    'сестре': 'https://podarki.ru/idei/Podarki-sestre-5859',
    'брату': 'https://podarki.ru/idei/Podarki-bratu-5860',
    'девушке': 'https://podarki.ru/idei/Chto-podarit-devushke-6082',
    'парню': 'https://podarki.ru/idei/Chto-podarit-parnyu-6081'
}

def parser(number, link):
    response = requests.get(f'{link}/{number}').text
    block = BeautifulSoup(response, "lxml")
    rows = block.find_all("div")
    gifts = []
    try:
        for row in rows:
            if row['class'][0] == 'good-card__name':
                gifts.append(row.text.replace('\xad', '').replace('\xa0', ' '))
    except Exception as error:
        pass
    return gifts[random.randrange(len(gifts))].lower()

def get_random_gift_idea(category):
    if category in categories:
        num = random.randrange(1, 3)
        link = categories[category]
        return parser(num, link)
    else:
        return None

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    markup.add(*[telebot.types.KeyboardButton(text=category.capitalize()) for category in categories.keys()])
    bot.send_message(chat_id=message.chat.id, text="Выберите для кого нужен подарок:", reply_markup=markup)
    
# Обработчик выбора категории
@bot.message_handler(func=lambda message: message.text.lower() in categories.keys())
def choose_category(message):
    category = message.text.lower()
    gift_idea = get_random_gift_idea(category)
    if gift_idea:
        response = f"Как насчет подарить {gift_idea} {category}?"
    else:
        response = "К сожалению, не удалось получить идею подарка. Попробуйте еще раз позже."
    bot.send_message(chat_id=message.chat.id, text=response)

# Запускаем бота
bot.polling()