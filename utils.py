from telebot import types

def generate_markup(list):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for i in list:
        markup.add(i)
    return markup