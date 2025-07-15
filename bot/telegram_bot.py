from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

from bot.weather import get_weather
from bot.time_utils import get_current_time
from bot.quotes import get_random_quote
from bot.horoscope import get_horoscope
from bot.attractions import get_attractions

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')  # Вставьте свой API ключ


# ---------------- Главное меню ----------------
def build_main_menu():
    keyboard = [
        [InlineKeyboardButton("📅 Время", callback_data="time")],
        [InlineKeyboardButton("☀️ Погода", callback_data="weather")],
        [InlineKeyboardButton("💬 Цитата дня", callback_data="quote")],
        [InlineKeyboardButton("🔮 Гороскоп", callback_data="horoscope")],
        [InlineKeyboardButton("🏛 Достопримечательности", callback_data="places")]
    ]
    return InlineKeyboardMarkup(keyboard)


async def show_main_menu(update_or_query, context):
    reply_markup = build_main_menu()
    if hasattr(update_or_query, "message"):
        await update_or_query.message.reply_text("Выберите действие:", reply_markup=reply_markup)
    elif hasattr(update_or_query, "edit_message_text"):
        await update_or_query.message.reply_text("Выберите действие:", reply_markup=reply_markup)


# ---------------- Старт ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот. Выберите опцию:", reply_markup=build_main_menu())


# ---------------- Обработка кнопок ----------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "time":
        context.user_data["awaiting"] = "time"
        await query.message.reply_text("Введите город для показа времени:", reply_markup=ReplyKeyboardRemove())

    elif query.data == "weather":
        context.user_data["awaiting"] = "weather"
        await query.message.reply_text("Введите город для погоды:", reply_markup=ReplyKeyboardRemove())

    elif query.data == "quote":
        await query.message.reply_text(get_random_quote())
        await show_main_menu(query, context)

    elif query.data == "horoscope":
        await show_zodiac_keyboard(query)

    elif query.data == "places":
        context.user_data["awaiting"] = "places"
        await query.message.reply_text("Введите город для поиска достопримечательностей:")


# ---------------- Ввод города ----------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get("awaiting")

    if mode == "weather":
        city = update.message.text
        await update.message.reply_text(get_weather(city))
        context.user_data["awaiting"] = None
        await show_main_menu(update, context)

    elif mode == "time":
        city = update.message.text
        await update.message.reply_text(get_current_time(city))
        context.user_data["awaiting"] = None
        await show_main_menu(update, context)

    elif mode == "places":
        city = update.message.text
        await update.message.reply_text("Ищу достопримечательности...")
        result = get_attractions(city)
        await update.message.reply_text(result)
        context.user_data["awaiting"] = None
        await show_main_menu(update, context)


# ---------------- Знаки зодиака ----------------
ZODIAC = {
    "aries": "♈ Овен", "taurus": "♉ Телец", "gemini": "♊ Близнецы",
    "cancer": "♋ Рак", "leo": "♌ Лев", "virgo": "♍ Дева",
    "libra": "♎ Весы", "scorpio": "♏ Скорпион", "sagittarius": "♐ Стрелец",
    "capricorn": "♑ Козерог", "aquarius": "♒ Водолей", "pisces": "♓ Рыбы"
}


async def show_zodiac_keyboard(query):
    keyboard = []
    keys = list(ZODIAC.items())
    for i in range(0, len(keys), 3):
        row = [
            InlineKeyboardButton(emoji, callback_data=f"sign:{sign}")
            for sign, emoji in keys[i:i + 3]
        ]
        keyboard.append(row)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Выберите ваш знак зодиака:", reply_markup=reply_markup)


# ---------------- Ответ по гороскопу ----------------
async def handle_zodiac(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("sign:"):
        sign = query.data.split(":")[1]
        result = get_horoscope(sign)
        await query.message.reply_text(result)
        await show_main_menu(query, context)


# ---------------- Запуск ----------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler, pattern="^(time|weather|quote|horoscope|places)$"))
    app.add_handler(CallbackQueryHandler(handle_zodiac, pattern="^sign:"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
