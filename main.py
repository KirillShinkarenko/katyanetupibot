#to install library: pip3 install pyTelegramBotAPI
import telebot

bot = telebot.TeleBot("347990160:AAFmDchqnN2V5i8haeJrosllTT1_mrTlbtw")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "hello")


@bot.message_handler(commands=['katya'])
def send_katy(message):
    bot.send_message(message.chat.id, "Katya two tomatos")


bot.polling()
