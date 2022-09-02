import telebot
from telebot import types
from config import TOKEN_1, exchanges
from extensions import Converter, APIException


def create_markup(base = None):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = []
    for val in exchanges.keys():
        if val != base:
            buttons.append(types.KeyboardButton(val.capitalize()))

    markup.add(*buttons)
    return markup


bot = telebot.TeleBot(TOKEN_1)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Приветствую Вас в виджете по конвертации валюты!\n \n\
Чтобы начать работу с виджетом введите /convert:\n \n\
Чтобы узнать все доступные для конвертации валюты введите: /value"
    bot.reply_to(message, text)


@bot.message_handler(commands=['value'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

# @bot.message_handler(content_types=['text'])
# def converter(message: telebot.types.Message):
#     try:
#         base, sym, amount = message.text.split()
#         amount = float(amount)
#     except ValueError as e:
#         bot.reply_to(message, 'Неверное количество параметров.')
#     try:
#         result = Converter.get_price(base, sym, amount)
#         bot.reply_to(message, f"Цена {amount} {base} в {sym} : {result}")
#     except APIException as e:
#         bot.reply_to(message, f"Ошибка в команде:\n{e}")

@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = 'Выберете валюту, из которой нужно конвертировать:'
    bot.reply_to(message, text, reply_markup=create_markup())
    bot.register_next_step_handler(message, base_handler)

def base_handler(message: telebot.types.Message):
    base = message.text.strip().lower()
    text = 'Выберете валюту, в которую хотите конвертировать:'
    bot.reply_to(message, text, reply_markup=create_markup(base))
    bot.register_next_step_handler(message, sym_handler, base)

def sym_handler(message: telebot.types.Message, base):
    sym = message.text.strip()
    text = 'Выберете количество валюты, которую хотите конвертировать:'
    bot.reply_to(message, text)
    bot.register_next_step_handler(message, amount_handler, base, sym)

def amount_handler(message: telebot.types.Message, base, sym):
    amount = message.text.strip()
    try:
        result = Converter.get_price(base, sym, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка конвертации: \n{e}")
    else:
        text = f"Цена {amount} {base} в {sym} : {result}"
        bot.reply_to(message, text)

bot.polling()

