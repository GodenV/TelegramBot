import datetime
import telebot
import os
import json

TOKEN = "626563305:AAEQBLLDERFUD2TgIRxwWK8uCtA7ONhAEFc"

bot = telebot.TeleBot(TOKEN)

GREETINGS = [
    "хай",
    "дороу",
    "привет",
    "дарова",
    "алё",
]

TRAINS = [
    "поезд",
    "колеса",
    "электон",
    "электричка",
]

@bot.message_handler(commands=["start", "help"])
def commands(message):
    bot.reply_to(message, "Привет")

@bot.message_handler(content_types=['text'])
def send_text(message):
    if ([i for i in GREETINGS if i in message.text.lower()]):
        bot.send_message(message.chat.id, 'Дороу?')
    elif ([i for i in TRAINS if i in message.text.lower()]):
        os.remove("quotes.json")
        os.system("scrapy runspider SpiderParser.py -o quotes.json")
        with open("quotes.json") as json_file:
            json_data = json.load(json_file)
            data = [i for i in json_data if (datetime.datetime.now().time().hour < int(i['time'][0][:2])) or ((datetime.datetime.now().time().hour == int(i['time'][0][:2])) and datetime.datetime.now().time().minute < int(i['time'][0][2:4]))]
        bot.send_message(message.chat.id,
        f"1.{data[0]['time'][0]} --- {data[0]['time'][1]} {data[0]['path']}\n"
        f"1.{data[1]['time'][0]} --- {data[1]['time'][1]} {data[1]['path']}\n"
        f"1.{data[2]['time'][0]} --- {data[2]['time'][1]} {data[2]['path']}\n")

if __name__ == "__main__":
    bot.polling()
