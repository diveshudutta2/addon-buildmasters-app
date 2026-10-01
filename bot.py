import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Render ke environment variables se token dynamically uthane ke liye
# (Yeh 'TELEGRAM_BOT_TOKEN' ya 'BOT_TOKEN' dono mein se jo bhi milega use utha lega)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN")

# Main Menu Keyboard Layout (4 Sections)
def get_main_menu_keyboard():
    keyboard = [
        [KeyboardButton("📢 Marketing"), KeyboardButton("🏢 Property")],
        [KeyboardButton("🏗️ Construction"), KeyboardButton("🛋️ Interior")]
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
            "Yahan aapko lead generation, promotional campaigns, aur social media management ki details milengi.\n"
            "*(Aage ka module yahan integrate kiya jayega)*"
        )
    elif text == "🏢 Property":
        response = (
            "🏢 **Property Section**\n\n"
            "Yahan properties listings, land details, aur commercial/residential plots ki information hogi.\n"
            "*(Aage ka module yahan integrate kiya jayega)*"
        )
    elif text == "🏗️ Construction":
        response = (
            "🏗️ **Construction Section**\n\n"
            "Turnkey construction projects, progress tracking, aur estimates yahan manage honge.\n"
            "*(Aage ka module yahan integrate kiya jayega)*"
        )
    elif text == "🛋️ Interior":
        response = (
            "🛋️ **Interior Section**\n\n"
            "Luxury interior designs, 3D elevations, aur material catalogs yahan show honge.\n"
            "*(Aage ka module yahan integrate kiya jayega)*"
        )
    else:
        response = "Kripya neeche diye gaye keyboard buttons ka hi upyog karein ya /start dabayein."

    await update.message.reply_text(response, parse_mode="Markdown")

def main():
    if not TOKEN:
        logger.error("❌ CRITICAL ERROR: Telegram Bot Token environment variable mein nahi mila!")
        return

    # Application build karein
    application = ApplicationBuilder().token(TOKEN).build()

    # Handlers add karein
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_menu_selection))

    # Bot ko start karein (Polling)
    logger.info("🚀 Addon Buildmasters Bot successfully start ho raha hai...")
    application.run_polling()

if __name__ == '__main__':
    main()
