# to install library: pip3 install pyTelegramBotAPI
import random
import urllib
import json
import codecs
import re
from datetime import time

import telebot

token = codecs.open("ne_tupi_token.txt", "r", "utf-8").read()
bot = telebot.TeleBot(token)
chatIds = codecs.open("ne_tupi_ids.txt", "r", "utf-8-sig").read()
chatIds = json.loads(chatIds)

logChatId = str(chatIds['logChatId'])
hardCoreChatId = str(chatIds['hardCoreChatId'])
kirillChatId = str(chatIds['kirillChatId'])
kateChatId = str(chatIds['kateChatId'])
lisaChatId = str(chatIds['lisaChatId'])

NON_LETTERS = re.compile('[^а-яё \-]+', flags=re.UNICODE)
ONLY_DASHES = re.compile('^\-+$', flags=re.UNICODE)
PREFIX = re.compile("^[бвгджзйклмнпрстфхцчшщьъ]+", flags=re.UNICODE)
vowels = {'о', 'е', 'а', 'я', 'у', 'ю', 'ы'}
rules = {'о': 'е', 'а': 'я', 'у': 'ю', 'ы': 'и'}

randPhrases = codecs.open("ne_tupi_phrases.txt", "r", "utf-8").read().split("\n")


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
        bot.send_message(lisaChatId, d)
    send_logs(message)


@bot.message_handler(commands=['ks'])
def send_katy(message):
    s = message.text
    d = s[4:]
    if d != "":
        bot.send_message(kirillChatId, d)
    else:
        bot.send_message(kirillChatId, 'lol kirill')


@bot.message_handler(commands=['kate'])
def send_katy(message):
    s = message.text
    d = message.text[5:]
    if d != "":
        bot.send_message(kateChatId, d)
    else:
        bot.send_message(kateChatId, 'oh wow')


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


@bot.message_handler(func=lambda message: True, content_types=['text'])
def huecho_msg(message):
    text_msg = message.text
    words = text_msg.split()
    try:
        if len(words) < 3:
            pass
        word = NON_LETTERS.sub("", words[-1].lower())
        if ONLY_DASHES.match(word):
            pass
        postfix = PREFIX.sub("", word)
        if word[:2] == "ху" and postfix[1] in rules.values():
            pass
        if len(postfix) < 3:
            pass
        if postfix[0] in rules:
            if postfix[1] not in vowels:
                huemessage = "ху%s%s" % (rules[postfix[0]], postfix[1:])
            else:
                if postfix[1] in rules:
                    huemessage = u"ху%s%s" % (rules[postfix[1]], postfix[2:])
                else:
                    huemessage = u'ху%s' % postfix[1:]
        else:
            huemessage = u"ху%s" % postfix

        if random.random() > 0.85:
            bot.send_message(message.chat.id, huemessage)
    except:
        pass


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
    current_temperature_nsu = str(nsu_json_dict['current'])
    temperature_to_message = message.from_user.first_name + ", вот твоя погода: " + current_temperature_nsu + u"\u00A0" + "°C"
    if message.from_user.username == "chagin_kv":
        temperature_to_message = "Погода спешл фор Чагин: " + "+69" + u"\u00A0" + "°C"
    bot.send_message(message.chat.id, temperature_to_message)
    send_logs(message)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_msg(message):
    user_name = message.from_user.first_name
    if user_name is None:
        user_name = message.from_user.first_name + message.from_user.last_name

    if user_name == "EkaterinaBerestova":
        if random.random() > 0.85:
            bot.send_message(message.chat.id, message.from_user.first_name + ", ты поняла?")

    if random.random() > 0.88:
        bot.send_message(message.chat.id, random.choice(randPhrases).format(user_name))


@bot.message_handler(func=lambda message: True, content_types=['text'])


def send_logs(message):
    chat_id = str(message.chat.id)
    user_name = message.from_user.username
    if user_name is None:
        user_name = message.from_user.first_name + message.from_user.last_name
    user_first_name = message.from_user.first_name
    message = message.text
    log = chat_id + " | " + user_name + " | " + message
    bot.send_message(logChatId, log)


bot.polling()