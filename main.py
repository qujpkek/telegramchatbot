from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
import telebot


bot = telebot.TeleBot(token='7411941828:AAGB81yK24ol0Nhc43J68U1XylVJQl7uqSo')

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Это тест приложение для мини приложений")

@bot.message_handler(commands=["start_miniapp"])
def start_miniapp(message):
    inline_keyboard_markup = InlineKeyboardMarkup()
    inline_keyboard_markup.row(InlineKeyboardButton("Запустить приложение", web_app=WebAppInfo("https://www.youtube.com/")))
    bot.reply_to(message, "Запусти приложение по кнопке снизу", reply_markup=inline_keyboard_markup)

bot.polling()
