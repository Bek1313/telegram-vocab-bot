from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import random
import os

# So'zlar ro'yxati
words = [
    ("apple", "olma"),
    ("book", "kitob"),
    ("car", "mashina"),
    ("water", "suv"),
    ("light", "yorug‘lik"),
    ("strong", "kuchli"),
    ("computer", "kompyuter"),
    ("happy", "baxtli"),
    ("fast", "tez"),
    ("school", "maktab"),
]

# Har foydalanuvchi uchun holatni saqlash
user_data = {}

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_data[user_id] = {
        "remaining": words.copy(),  # yangi, tasodifiy so'zlar shu yerda ishlatiladi
        "current": None
    }
    update.message.reply_text("Assalomu alaykum! Boshladik!\nYangi so'z uchun /word buyrug'ini yuboring.")

def get_word(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in user_data:
        start(update, context)
    
    if not user_data[user_id]["remaining"]:
        # Barcha so‘zlar ko‘rilgan — ro‘yxat yangilanadi
        user_data[user_id]["remaining"] = words.copy()
        update.message.reply_text("👏 Barcha so‘zlarni ko‘rib chiqdik! Endi qaytadan boshlaymiz.")

    # Tasodifiy so‘z tanlanadi
    selected = random.choice(user_data[user_id]["remaining"])
    user_data[user_id]["remaining"].remove(selected)
    user_data[user_id]["current"] = selected

    # Inglizcha yoki o‘zbekcha — tasodifiy tanlab chiqaramiz
    if random.choice([True, False]):
        word_to_show = selected[0]
        lang = "EN"
    else:
        word_to_show = selected[1]
        lang = "UZ"

    keyboard = [
        [InlineKeyboardButton("Tarjimasini ko‘rsat", callback_data="show")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f"So‘z ({lang}): *{word_to_show}*", parse_mode="Markdown", reply_markup=reply_markup)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()

    if user_id in user_data and user_data[user_id]["current"]:
        en, uz = user_data[user_id]["current"]
        query.edit_message_text(text=f"{en} — {uz}")
    else:
        query.edit_message_text(text="So‘z topilmadi. Iltimos, /word buyrug‘ini bering.")

def main():
    TOKEN = os.getenv("7859530337:AAFtVShiQa9aZlrlSrS0N4t1ukJwXKJDyxQ")
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("word", get_word))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
