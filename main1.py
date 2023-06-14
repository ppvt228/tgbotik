import telebot
import random
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
# эта тема помогает создать разные штуки для клавиатуры телеграма, типа тех же кнопок в дайвинчике и прочая шняга
from telebot import types

with open('token.txt', 'r') as file:
    bot_token = file.read().strip()
bot = telebot.TeleBot(token=bot_token)

# with open('yandexapi.txt', 'r') as file:
#     YANDEX_API_KEY = file.read().strip()

# print(YANDEX_API_KEY) # test message


# # Список идей в виде словаря, можно добавлять вручную че хочешь
# ideas = {
#     'сестре': ['швабру', 'средство для мытья посуды', 'карту до кухни', 'губку для мытья посуды'],
#     'брату': ['гаджет', 'спортивные товары', 'игру', 'футболку любимой команды'],
#     'девушке': ['половник', 'кастрюлю', 'средство для мытья полов', 'уголь'],
#     'парню': ['инструменты', 'наушники', 'одежду', 'аксессуары для авто']
# }

# # Тут /start и создание кнопок для выбора в тг
# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
#     markup.add(*[types.KeyboardButton(text=category.capitalize()) for category in ideas.keys()])
#     bot.send_message(chat_id=message.chat.id, text="Выберите для кого нужен подарок:", reply_markup=markup)

# # Обработчик выбора категории, но не работает часть с else, это надо исправить, по идее из за первой же строчки и не работает
# @bot.message_handler(func=lambda message: message.text.lower() in ideas.keys())
# def choose_category(message):
#     category = message.text.lower()
#     if category in ideas:
#         gift_ideas = ideas[category]
#         gift_idea = random.choice(gift_ideas)
#         response = f"Подарите {category} {gift_idea}"
#     else:
#         response = "К сожалению, у меня нет идей для такого человека."
#     bot.send_message(chat_id=message.chat.id, text=response)

# # Запускаем бота
# bot.polling()





# Список категорий подарков
categories = {
    'сестре': 'https://podarki.ru/idei/Podarki-sestre-5859',
    'брату': 'https://podarki.ru/idei/Podarki-bratu-5860',
    'девушке': 'https://podarki.ru/idei/Chto-podarit-devushke-6082',
    'парню': 'https://podarki.ru/idei/Chto-podarit-parnyu-6081'
}

# Функция для получения случайной идеи подарка с помощью поиска в Яндексе
# def get_random_gift_idea(category):
#     query = categories[category]
#     url = f"https://yandex.com/search/xml?user={YANDEX_API_KEY}&key={YANDEX_API_KEY}&query={query}&l10n=en&sortby=rlv"
#     response = requests.get(url)
#     response.raise_for_status()

#     xml_response = response.text
#     print(xml_response) # testing message

#     # Парсинг XML-ответа и извлечение идеи подарка
#     root = ET.fromstring(xml_response)
#     items = root.findall('.//item')
#     print(items) # testing message
#     if items:
#         random_item = random.choice(items)
#         gift_idea = random_item.find('title').text
#         return gift_idea
#     else:
#         return None

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