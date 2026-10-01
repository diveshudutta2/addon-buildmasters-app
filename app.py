import os
import threading
import logging
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Addon Buildmasters Bot & Web Server is running live on Render! 🚀"

# Telegram Bot Token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN")


# Main Menu
def get_main_menu_keyboard():
    keyboard = [
        [KeyboardButton("📢 Marketing"), KeyboardButton("🏗️ Construction")],
        [KeyboardButton("🏢 Property"), KeyboardButton("🛋️ Interior")]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        input_field_placeholder="Please choose a section..."
    )


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = (
        update.effective_user.first_name
        if update.effective_user
        else "Ji"
    )

    welcome_message = (
        f"Namaste {user_name} ji! 🙏\n\n"
        "Welcome to **Addon Buildmasters Bot**.\n"
        "Aapki construction aur interior services ko manage karne ke liye "
        "main taiyar hoon.\n\n"
        "Neeche diye gaye sections mein se koi option chunein:"
    )

    await update.message.reply_text(
        welcome_message,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="Markdown"
    )


# Menu Selection
async def handle_menu_selection(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    text = update.message.text

    if text == "📢 Marketing":
        response = (
            "📢 **Marketing Section**\n\n"
            "• Lead generation & campaigns\n"
            "• Social media & Google Business Profile management\n"
            "• Content & marketing automation"
        )

    elif text == "🏗️ Construction":
        response = (
            "🏗️ **Construction Section**\n\n"
            "• Turnkey construction projects\n"
            "• Progress tracking & site updates\n"
            "• Cost estimates & material tracking"
        )

    elif text == "🏢 Property":
        response = (
            "🏢 **Property Section**\n\n"
            "• Commercial & residential plots\n"
            "• Land listings\n"
            "• Property dealing & legal details"
        )

    elif text == "🛋️ Interior":
        response = (
            "🛋️ **Interior Section**\n\n"
            "• Luxury interior design\n"
            "• Modern 3D elevations & renders\n"
            "• Modular kitchen & home interiors\n"
            "• Quotations"
        )

    else:
        response = (
            "Kripya neeche diye gaye keyboard buttons ka hi "
            "upyog karein ya /start dabayein."
        )

    await update.message.reply_text(
        response,
        parse_mode="Markdown"
    )


# Telegram Bot
def run_telegram_bot():
    if not TOKEN:
        logger.error(
            "❌ Telegram Bot Token environment variable mein nahi mila!"
        )
        return

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & (~filters.COMMAND),
            handle_menu_selection
        )
    )

    logger.info("🚀 Addon Buildmasters Telegram Bot started...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


# Main
if __name__ == "__main__":

    if TOKEN:
        bot_thread = threading.Thread(
            target=run_telegram_bot,
            daemon=True
        )
        bot_thread.start()
        logger.info("🚀 Telegram Bot running in background...")
    else:
        logger.warning(
            "⚠️ Bot token absent. Running web server only."
        )

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
