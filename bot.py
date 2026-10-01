import os
import threading
import logging
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Flask App setup (Render ke liye zaroori web server)
app = Flask(__name__)

@app.route('/')
def home():
    return "Addon Buildmasters Bot & Web Server is running live on Render! 🚀"

# Telegram Bot Token (Render Environment Variables se uthayega)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN")

# Main Menu Keyboard Layout (4 Sections)
def get_main_menu_keyboard():
    keyboard = [
        [KeyboardButton("📢 Marketing"), KeyboardButton("🏗️ Construction")],
        [KeyboardButton("🏢 Property"), KeyboardButton("🛋️ Interior")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, input_field_placeholder="Please choose a section...")

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name if update.effective_user else "Ji"
    welcome_message = (
        f"Namaste {user_name} ji! 🙏\n\n"
        "Welcome to **Addon Buildmasters Bot**.\n"
        "Aapki construction aur interior services ko manage karne ke liye main taiyar hoon. "
        "Neeche diye gaye sections mein se koi option chunein:"
    )
    await update.message.reply_text(
        welcome_message, 
        reply_markup=get_main_menu_keyboard(), 
        parse_mode="Markdown"
    )

# Menu sections ke liye message handler
async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "📢 Marketing":
        response = (
            "📢 **Marketing Section**\n\n"
            "• Lead generation & campaigns\n"
            "• Social media & Google Business Profile (GMB) management\n"
            "*(Aage ka module yahan integrate kiya jayega)*"
        )
    elif text == "🏗️️ Construction":
        response = (
            "🏗️ **Construction Section**\n\n"
            "• Turnkey construction projects\n"
            "• Progress tracking & site updates\n"
            "• Cost estimates & material tracking\n"
            "*(Aage ka module yahan integrate kiya jayega)*"
        )
    elif text == "🏢 Property":
        response = (
            "🏢 **Property Section**\n\n"
            "• Commercial & residential plots\n"
            "• Land listings & legal details (jaise HP Section 118)\n"
            "*(Aage ka module yahan integrate kiya jayega)*"
        )
    elif text == "🛋️ Interior":
        response = (
            "🛋️️ **Interior Section**\n\n"
            "• Luxury interior design catalogs\n"
            "• Modern 3D elevations & space renders\n"
            "• Showroom/Home decor quotations\n"
            "*(Aage ka module yahan integrate kiya jayega)*"
        )
    else:
        response = "Kripya neeche diye gaye keyboard buttons ka hi upyog karein ya /start dabayein."

    await update.message.reply_text(response, parse_mode="Markdown")

# Telegram Bot Runner Function (Background Thread)
def run_telegram_bot():
    if not TOKEN:
        logger.error("❌ CRITICAL ERROR: Telegram Bot Token environment variable mein nahi mila!")
        return

    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_menu_selection))

    logger.info("🚀 Addon Buildmasters Bot polling start ho raha hai...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    # Telegram bot ko background thread mein chalaein taaki port conflict na ho
    if TOKEN:
        bot_thread = threading.Thread(target=run_telegram_bot)
        bot_thread.daemon = True
        bot_thread.start()
        logger.info("🚀 Starting Telegram Bot in Background...")
    else:
        logger.warning("⚠ Warning: Bot token absent, running web server only.")

    # Flask Server (Main thread)
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
