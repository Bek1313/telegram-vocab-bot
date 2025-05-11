from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import random

# So'zlar ro'yxati
words = [
    ("allow", "ruxsat"),
    ("notebook", "daftar"),
    ("sun", "quyosh"),
    ("watermelon", "qovun"),
    ("car", "mashina")
]

# Har bir foydalanuvchi uchun so'zlar tarixini saqlash
user_data = {}

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_data[user_id] = {
        "shown": [],
        "current": None
    }
    send_new_word(update, context)

def send_new_word(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    shown = user_data[user_id]["shown"]

    remaining = [pair for pair in words if pair not in shown]

    if not remaining:
        update.message.reply_text("Barcha so‘zlarni ko‘rdingiz!")
        return

    word_pair = random.choice(remaining)
    user_data[user_id]["shown"].append(word_pair)
    user_data[user_id]["current"] = word_pair

    english_word = word_pair[0]
    keyboard = [[InlineKeyboardButton("Tarjimasi", callback_data="translate")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(english_word, reply_markup=reply_markup)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()

    if query.data == "translate":
        _, uzbek = user_data[user_id]["current"]
        query.edit_message_text(text=f"Tarjimasi: {uzbek}")

def next_command(update: Update, context: CallbackContext):
    send_new_word(update, context)

def main():
    updater = Updater("7859530337:AAFtVShiQa9aZlrlSrS0N4t1ukJwXKJDyxQ", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("next", next_command))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
