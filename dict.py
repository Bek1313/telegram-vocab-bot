from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import random

# So'zlar ro'yxati (siz keyinchalik fayldan yoki xabar orqali yuklab qo'shasiz)
words = [
    ("apple", "olma"),
    ("sun", "quyosh"),
    ("book", "kitob"),
    ("water", "suv"),
    # ...
]

current_word = {}  # Har bir foydalanuvchi uchun alohida

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Salom! 'next' buyrug‘ini yuboring yoki /next deb yozing.")

def next_word(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    word = random.choice(words)
    current_word[user_id] = word

    # Ingliz yoki o‘zbek so‘zini ko‘rsatish (tasodifiy)
    if random.choice([True, False]):
        display_word = word[0]  # English
        lang = "Inglizcha"
    else:
        display_word = word[1]  # Uzbek
        lang = "O'zbekcha"

    keyboard = [[InlineKeyboardButton("Tarjimani ko‘rish", callback_data='show_translation')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(f"{lang} so‘z: *{display_word}*", parse_mode="Markdown", reply_markup=reply_markup)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id

    if query.data == 'show_translation':
        word = current_word.get(user_id)
        if word:
            query.edit_message_text(text=f"Inglizcha: *{word[0]}*\nO‘zbekcha: *{word[1]}*", parse_mode="Markdown")
        else:
            query.edit_message_text("Avval /next buyrug‘ini yuboring.")

def main():
    updater = Updater("7859530337:AAFtVShiQa9aZlrlSrS0N4t1ukJwXKJDyxQ", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("next", next_word))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
