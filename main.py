# to install library: pip3 install pyTelegramBotAPI
import random
import urllib
import json
import codecs
import re
import datetime
import time

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
chbuChatId = str(chatIds['chbuChatId'])

NON_LETTERS = re.compile('[^а-яё \-]+', flags=re.UNICODE)
ONLY_DASHES = re.compile('^\-+$', flags=re.UNICODE)
PREFIX = re.compile("^[бвгджзйклмнпрстфхцчшщьъ]+", flags=re.UNICODE)
vowels = {'о', 'е', 'а', 'я', 'у', 'ю', 'ы'}
rules = {'о': 'е', 'а': 'я', 'у': 'ю', 'ы': 'и'}

randPhrases = codecs.open("ne_tupi_phrases.txt", "r", "utf-8").read().split("\n")
randNeurals = codecs.open("ne_tupi_neurals.txt", "r", "utf-8").read().split("\n")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Bomjur")


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


@bot.message_handler(commands=['weather'])
def send_weather_nsu(message):
    bot.send_message(message.chat.id, 'Норм бот тут: @weather_vz_bot')
    send_logs(message)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def huecho_msg(message):
    huendom = random.random()
    text_msg = message.text
    words = text_msg.split()
    user_name = message.from_user.first_name
    if user_name is None:
        user_name = message.from_user.first_name + message.from_user.last_name
    if str(text_msg).lower() == 'нет':
        bot.send_message(message.chat.id, 'пидора ответ')
    if str(text_msg).lower() == 'да':
        bot.send_message(message.chat.id, 'винда')
    if 0.75 < huendom < 0.8:
        bot.send_message(message.chat.id, random.choice(randPhrases).format(user_name))
    if 0.65 < huendom < 0.67:
        bot.send_message(message.chat.id, random.choice(randNeurals).format(user_name))
    if huendom > 0.95:
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
            bot.send_message(message.chat.id, huemessage)
        except:
            pass


@bot.message_handler(func=lambda message: True, content_types=['text'])
def send_logs(message):
    chat_id = str(message.chat.id)
    user_name = message.from_user.username
    if user_name is None:
        user_name = message.from_user.first_name + message.from_user.last_name
    message = message.text
    log = chat_id + " | " + user_name + " | " + message
    bot.send_message(logChatId, log)


def bot_launch():
    try:
        if __name__ == '__main__':
            bot.polling(none_stop=True)
    except:
        time.sleep(60)
        bot_launch()


bot_launch()
