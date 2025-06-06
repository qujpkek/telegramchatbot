import telebot
import random
import os

bot = telebot.TeleBot("token")
memes = os.listdir("pictures")

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши что-нибудь!")

@bot.message_handler(commands=["meme"])
def send_pictures(message):
    with open(f"pictures/{random.choice(memes)}", 'rb') as f:
        bot.send_photo(message.chat.id, f)

@bot.message_handler(commands=["animals"])
def send_pictures(message):
    while True:
        meme = random.choice(memes)
        if 'animal' in meme:
            break
    
    with open(f"pictures/{meme}", 'rb') as f:
        bot.send_photo(message.chat.id, f)

bot.polling()
