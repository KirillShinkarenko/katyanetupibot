# to install library: pip3 install pyTelegramBotAPI
import random
import urllib
import json
import codecs
from datetime import time

import telebot
from bs4 import BeautifulSoup

token = codecs.open("ne_tupi_token.txt", "r", "utf-8").read()
bot = telebot.TeleBot("347990160:AAFkHTWEjTJ0_XuE0Lqaqi0aIvEAD5ImRZk")
logChatId = -281676857
hardCoreChatId = -1001141052816
kirillChatId = 241118222
kateChatId = 287805371

randPhrases = ["{}, больной ублюдок",
               "{}, что ты несешь?",
               "{}, не хочешь бухнуть сегодня?",
               'мда, {}, мда',
               "{}, с тебя 100 рублей в копилку"
               "{}, спорим на соточку?",
               "{}, ты просто 🐽",
               "Забудь, {}",
               "Э, {}!",
               "{}, ну не тупи"]


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Bomjur")
    send_logs(message)


@bot.message_handler(commands=['getChatId'])
def send_katy(message):
    bot.send_message(message.chat.id, "такой: " + str(message.chat.id))
    send_logs(message)


@bot.message_handler(commands=['v'])
def send_katy(message):
    s = message.text
    d = s[3:]
    if d != "":
        bot.send_message(hardCoreChatId, d)
    send_logs(message)

@bot.message_handler(commands=['l'])
def send_katy(message):
    s = message.text
    d = s[3:]
    if d != "":
        bot.send_message(251478838, d)
    send_logs(message)


@bot.message_handler(commands=['ks'])
def send_katy(message):
    s = message.text
    d = s[4:]
    if d != "":
        bot.send_message(kirillChatId, d)
    else:
        bot.send_message(kirillChatId, 'oh wow')
    send_logs(message)


@bot.message_handler(commands=['kate'])
def send_katy(message):
    s = message.text
    d = message.text[5:]
    if d != "":
        bot.send_message(kateChatId, d)
    send_logs(message)

@bot.message_handler(commands=['ping'])
def perform_ping(message):
    bot.send_message(message.chat.id, "Себя попингуй")


@bot.message_handler(commands=['vo'])
def send_katy(message):
    s = message.text
    d = s[4:]
    if d != "":
        bot.send_message(logChatId, d)
    send_logs(message)


@bot.message_handler(commands=['weather'])
def send_weather_nsu(message):
    try:
        usock = urllib.request.urlopen("http://nsuweather.appspot.com/full", data=None)
    except:
        bot.send_message(message.chat.id, "Сайт лежит, подожди :)")
        time.sleep(10)
        send_weather_nsu(message)

    nsu_json_string = usock.read()
    nsu_json_dict = json.loads(nsu_json_string)
    current_temperature_nsu = str(nsu_json_dict ['current'])
    temperature_to_message = message.from_user.first_name + ", вот твоя погода: " + current_temperature_nsu + " °C"
    if message.from_user.username == "chagin_kv":
        temperature_to_message = message.from_user.first_name + ", вот твоя погода: " + "+69" + " °C"
    bot.send_message(message.chat.id, temperature_to_message)
    send_logs(message)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_msg(message):
    user_name = message.from_user.first_name
    if random.random() > 0.95:
        bot.send_message(message.chat.id, random.choice(randPhrases).format(user_name))


def send_logs(message):
    chat_id = str(message.chat.id)
    user_name = message.from_user.username
    user_first_name = message.from_user.first_name
    message = message.text
    log = chat_id + " | " + user_name + " | " + message
    bot.send_message(logChatId, log)



bot.polling()