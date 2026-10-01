import os
import logging
import threading
from flask import Flask, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    MessageHandler, filters, ContextTypes, ConversationHandler
)

# Logging setup
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Universal Owner PIN
OWNER_PIN = "1704"

# Conversation States for Authentication & Lead Gen
WAITING_FOR_PASSWORD = 1
ASK_NAME, ASK_PHONE, ASK_SERVICE = range(2, 5)

# --- FLASK APP (Runs in Background Thread for Render Port Binding) ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Addon Buildmasters SEO Intelligence Bot is live and running! 🚀", 200

@app.route("/health")
def health():
    return jsonify({"status": "active", "service": "GMB SEO Audit Bot"}), 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"Starting Flask server on port {port}...")
    app.run(host="0.0.0.0", port=port, use_reloader=False)


# --- AUTHENTICATION & START HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Reset session state
    context.user_data['authenticated'] = False
    
    await update.message.reply_text(
        "🔐 **Welcome to Addon Buildmasters Private Limited**\n\n"
        "Please enter the secure universal password to access the company intelligence system:",
        parse_mode="Markdown"
    )
    return WAITING_FOR_PASSWORD

async def verify_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password_input = update.message.text.strip()
    
    if password_input == OWNER_PIN:
        context.user_data['authenticated'] = True
        await show_main_menu(update, context, is_new_message=True)
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            "❌ **Incorrect Password!** Access Denied.\n"
            "Please try again by typing `/start` or entering the correct PIN:",
            parse_mode="Markdown"
        )
        return WAITING_FOR_PASSWORD


# --- MAIN MENU WITH MARKETING, OPERATIONS, FINANCE ---
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, is_new_message=False):
    keyboard = [
        [InlineKeyboardButton("📈 Marketing (GMB & SEO Audit)", callback_data="sec_marketing")],
        [InlineKeyboardButton("⚙️ Operations (Projects & Lead Gen)", callback_data="sec_operations")],
        [InlineKeyboardButton("💰 Finance (Billing & Reports)", callback_data="sec_finance")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "🏢 **Addon Buildmasters Private Limited - Dashboard**\n\n"
        "Select a department section below to proceed:"
    )
    
    if is_new_message:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode="Markdown")


# --- SECTION HANDLERS (Marketing, Operations, Finance) ---
async def handle_sections(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "sec_marketing":
        keyboard = [
            [InlineKeyboardButton("🔍 Run GMB SEO Audit (Priority #1)", callback_data="run_seo_audit")],
            [InlineKeyboardButton("📊 Full Business Scorecard", callback_data="full_scorecard")],
            [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
        ]
        await query.edit_message_text(
            text="📈 **MARKETING SECTION**\n\nManage your local SEO, GMB rankings, and visibility for Dharamshala & Kangra:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        
    elif data == "sec_operations":
        keyboard = [
            [InlineKeyboardButton("📝 Generate New Client Lead", callback_data="start_lead")],
            [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
        ]
        await query.edit_message_text(
            text="⚙️ **OPERATIONS SECTION**\n\nHandle project execution tracking and automated lead generation inquiries:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        
    elif data == "sec_finance":
        keyboard = [
            [InlineKeyboardButton("📊 View Financial Reports / Invoices", callback_data="view_finance")],
            [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
        ]
        await query.edit_message_text(
            text="💰 **FINANCE SECTION**\n\nTrack company billing, accounting summaries, and tax compliance registers:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        
    elif data == "main_menu":
        await show_main_menu(update, context)


# --- GMB SEO AUDIT ENGINE (Priority #1) ---
async def run_seo_audit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    audit_data = {
        "seo_score": 85,
        "breakdown": {
            "Primary Keyword in Business Title": {"status": "Pass", "points": "15/15", "tip": "Title correctly targets Turnkey & Interiors."},
            "Geotagged Photos & Regular Posts": {"status": "Needs Attention", "points": "12/20", "tip": "Upload weekly 3D elevation renders with Dharamshala tags."},
            "Reviews Velocity & Keywords Response": {"status": "Good", "points": "18/20", "tip": "Maintain <24hr reply rate using local keywords."},
            "NAP Consistency (Name, Address, Phone)": {"status": "Pass", "points": "15/15", "tip": "Synced across all business directories."},
            "Service List & Description Optimization": {"status": "Good", "points": "25/30", "tip": "Enhance description with luxury interior keywords."}
        }
    }
    
    response_text = (
        f"🎯 *PRIORITY #1: GMB SEO AUDIT & MARKING*\n"
        f"🏢 *Company:* Addon Buildmasters Pvt Ltd\n"
        f"⭐ *SEO Score:* `{audit_data['seo_score']}/100` (Grade: A)\n\n"
        f"📋 *Detailed SEO Parameter Breakdown:*\n"
    )
    
    for param, details in audit_data['breakdown'].items():
        icon = "✅" if details['status'] == "Pass" else "⚠️" if details['status'] == "Good" else "🔧"
        response_text += f"{icon} *{param}* — `{details['points']}`\n   💡 *Tip:* {details['tip']}\n\n"
        
    keyboard = [[InlineKeyboardButton("🔙 Back to Marketing", callback_data="sec_marketing")]]
    await query.edit_message_text(text=response_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")


# --- MAIN ENTRY POINT ---
def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN environment variable is missing!")
        return

    # Start Flask server in background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Telegram Bot Setup
    application = Application.builder().token(TOKEN).build()

    # Password Authentication Handler
    auth_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAITING_FOR_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, verify_password)]
        },
        fallbacks=[CommandHandler("start", start)]
    )

    application.add_handler(auth_handler)
    application.add_handler(CallbackQueryHandler(handle_sections, pattern="^sec_|^main_menu"))
    application.add_handler(CallbackQueryHandler(run_seo_audit, pattern="^run_seo_audit$"))

    logger.info("Telegram Bot started polling in main thread...")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
