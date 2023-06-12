import telebot
import random
# эта тема помогает создать разные штуки для клавиатуры телеграма, типа тех же кнопок в дайвинчике и прочая шняга
from telebot import types

bot_token = 'token'
bot = telebot.TeleBot(token=bot_token)

# Список идей в виде словаря, можно добавлять вручную че хочешь
ideas = {
    'сестре': ['швабру', 'средство для мытья посуды', 'карту до кухни', 'губку для мытья посуды'],
    'брату': ['гаджет', 'спортивные товары', 'игру', 'футболку любимой команды'],
    'девушке': ['половник', 'кастрюлю', 'средство для мытья полов', 'уголь'],
    'парню': ['инструменты', 'наушники', 'одежду', 'аксессуары для авто']
}

# Тут /start и создание кнопок для выбора в тг
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    markup.add(*[types.KeyboardButton(text=category.capitalize()) for category in ideas.keys()])
    bot.send_message(chat_id=message.chat.id, text="Выберите для кого нужен подарок:", reply_markup=markup)

# Обработчик выбора категории, но не работает часть с else, это надо исправить, по идее из за первой же строчки и не работает
@bot.message_handler(func=lambda message: message.text.lower() in ideas.keys())
def choose_category(message):
    category = message.text.lower()
    if category in ideas:
        gift_ideas = ideas[category]
        gift_idea = random.choice(gift_ideas)
        response = f"Подарите {category} {gift_idea}"
    else:
        response = "К сожалению, у меня нет идей для такого человека."
    bot.send_message(chat_id=message.chat.id, text=response)

# Запускаем бота
bot.polling()