import datetime
import telebot
import os
import json
import config
import dbworker
import utils
bot = telebot.TeleBot(config.TOKEN)

status = 0

@bot.message_handler(commands=["start"])
def cmd_start(message):
    markup = utils.generate_markup(["Погода", "Электрички"])
    bot.send_message(message.chat.id, "Привет, выбирай пункт", reply_markup=markup)
    dbworker.set_state(message.chat.id, config.States.MAIN_SELECT.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.MAIN_SELECT.value)
def user_entering_name(message):
    if "Назад" == message.text:
        dbworker.set_state(message.chat.id, config.States.SELECT_RULES.value)
    elif "Электрички" == message.text:
        markup = utils.generate_markup(["Минск -- Моло", "Моло -- Минск", "Назад"])
        bot.send_message(message.chat.id, "Выберите маршрут!", reply_markup=markup)
        dbworker.set_state(message.chat.id, config.States.SELECT_RULES.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.SELECT_RULES.value)
def select_rule(message):
    # if ([i for i in GREETINGS if i in message.text.lower()]):
    #     bot.send_message(message.chat.id, 'Що нада бля?')
    # elif ([i for i in TRAINS if i in message.text.lower()]):
        if "Назад" == message.text:
            dbworker.set_state(message.chat.id, config.States.MAIN_SELECT.value)
        elif "Моло -- Минск" == message.text:
            os.remove("quotes.json")
            print(os.system("scrapy crawl Pavuk -o quotes.json -a url=molodechno--minsk"))
        elif "Минск -- Моло" == message.text:
            os.remove("quotes.json")
            print(os.system("scrapy crawl Pavuk -o quotes.json -a url=minsk--molodechno"))
        try:
            with open("quotes.json") as json_file:
                json_data = json.load(json_file)
                print(json_data[0]['time'][0][3:5])
                data = [i for i in json_data if (datetime.datetime.now().time().hour < int(i['time'][0][:2])) or ((datetime.datetime.now().time().hour == int(i['time'][0][:2])) and datetime.datetime.now().time().minute < int(i['time'][0][3:5]))]
                if not data:
                    data = json_data[:3]
                bot.send_message(message.chat.id,
                f"1. {data[0]['time'][0]} --- {data[0]['time'][1]} {data[0]['path']}\n"
                f"2. {data[1]['time'][0]} --- {data[1]['time'][1]} {data[1]['path']}\n"
                f"3. {data[2]['time'][0]} --- {data[2]['time'][1]} {data[2]['path']}\n")
        except IOError:
            pass
if __name__ == "__main__":
    bot.polling()
