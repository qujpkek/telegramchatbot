from ecobot_questions import questions
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot
import random

bot = telebot.TeleBot("tutifruti")

user_data = {}

def gen_markup(question):
    markup = InlineKeyboardMarkup()
    for option in question["options"]:
        markup.add(InlineKeyboardButton(option, callback_data=option))
    return markup

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я ЭКО-бот. Напиши /victorina, чтобы начать викторину 🌍")

@bot.message_handler(commands=["victorina"])
def send_victorina(message):
    user_id = message.from_user.id
    user_data[user_id] = {
        "lives": 3,
        "strike": 0,
        "answered": [],
        "current_question": None
    }

    bot.send_message(message.chat.id, "Начинаем викторину! У тебя 3 жизни 💚")
    send_next_question(message.chat.id, user_id)

def send_next_question(chat_id, user_id):
    data = user_data[user_id]

    if data["lives"] <= 0:
        bot.send_message(chat_id, f"😢 Ты проиграл! Страйк: {data['strike']}")
        return

    available_questions = [q for q in questions if q["question"] not in data["answered"]]
    if not available_questions:
        bot.send_message(chat_id, f"🎉 Поздравляем! Ты ответил на все вопросы. Страйк: {data['strike']}")
        return

    question = random.choice(available_questions)
    data["current_question"] = question
    data["answered"].append(question["question"])

    bot.send_message(chat_id, f"🧠 {question['question']}", reply_markup=gen_markup(question))

@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    user_id = call.from_user.id
    if user_id not in user_data:
        bot.answer_callback_query(call.id, "Сначала напиши /victorina")
        return

    data = user_data[user_id]
    question = data["current_question"]

    if not question:
        bot.answer_callback_query(call.id, "Нет активного вопроса.")
        return

    selected = call.data
    if selected == question["answer"]:
        data["strike"] += 1
        bot.answer_callback_query(call.id, "✅ Правильно!")
    else:
        data["lives"] -= 1
        bot.answer_callback_query(call.id, f"❌ Неправильно! Осталось жизней: {data['lives']}")

    send_next_question(call.message.chat.id, user_id)

bot.polling()
