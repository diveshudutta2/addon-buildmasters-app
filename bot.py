import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states for Property Search
LOCATION, PRICE, PROPERTY_TYPE = range(3)

# Bot Token & Owner PIN (Aap apne environment variables ya config se le sakte hain)
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")

# --- START / MAIN MENU ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🏢 Property Search", callback_data="menu_property_search")],
        [InlineKeyboardButton("📊 SEO Rankings & Reports", callback_data="menu_seo")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "👋 **Welcome to Addon Buildmasters Management Bot**\n\n"
        "Naye update ke mutabiq, ab aap yahan se direct **Property Search & Data Extraction** kar sakte hain."
    )
    
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# --- PROPERTY SEARCH CONVERSATION FLOW ---
async def property_search_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="🔍 **Property Search Module**\n\nKripya target **Location** enter karein (e.g., Dharamshala, New Delhi, Chandigarh):",
        parse_mode="Markdown"
    )
    return LOCATION

async def receive_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['location'] = update.message.text
    await update.message.reply_text(
        "💰 Ab **Price Range** specify karein (e.g., 50L to 1.5Cr, Under 1Cr):"
    )
    return PRICE

async def receive_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['price'] = update.message.text
    
    keyboard = [
        [InlineKeyboardButton("🏠 Residential", callback_data="type_residential")],
        [InlineKeyboardButton("🏢 Commercial", callback_data="type_commercial")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🏗️ Kripya **Property Type** select karein:",
        reply_markup=reply_markup
    )
    return PROPERTY_TYPE

async def receive_type_and_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    prop_type = "Residential" if "residential" in query.data else "Commercial"
    context.user_data['property_type'] = prop_type
    
    loc = context.user_data.get('location', 'Unknown')
    price = context.user_data.get('price', 'N/A')
    
    await query.edit_message_text(
        text=f"⏳ **Searching properties across sites...**\n\n📍 Location: {loc}\n💵 Budget: {price}\n🏷️ Type: {prop_type}\n\nKripya thoda intezaar karein, results fetch ho rahe hain...",
        parse_mode="Markdown"
    )
    
    # Mock / Scraped Real Estate Results (Yahan aap BeautifulSoup ya APIs connect kar sakte hain)
    properties = [
        {
            "title": f"Prime {prop_type} Space in {loc}",
            "price": price,
            "details": "Modern 3D Elevation layout, high ROI potential, immediate registry available.",
            "source_link": f"https://realestate-aggregator.com/search?loc={loc}&type={prop_type}"
        },
        {
            "title": f"Luxury Independent {prop_type} Unit",
            "price": price,
            "details": "Prime roadside access, premium interior finish, spacious layout.",
            "source_link": f"https://realestate-aggregator.com/listing/{loc}-02"
        }
    ]
    
    context.user_data['last_results'] = properties
    
    # Results display
    result_text = f"✅ **Found {len(properties)} Properties for {loc}:**\n\n"
    keyboard = []
    
    for idx, prop in enumerate(properties):
        result_text += f"*{idx+1}. {prop['title']}*\n💰 Price: {prop['price']}\n📝 {prop['details']}\n\n"
        keyboard.append([InlineKeyboardButton(f"📥 Download Details (Prop #{idx+1})", callback_data=f"download_prop_{idx}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=result_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return ConversationHandler.END

# --- PDF GENERATOR & DOWNLOAD HANDLER ---
def generate_pdf(prop_data, filename="property_details.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Header Banner
    c.setFillColorRGB(0.1, 0.2, 0.4)
    c.rect(0, height - 80, width, 80, fill=1, stroke=0)
    
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, height - 45, "ADDON BUILDMASTERS - PROPERTY REPORT")
    
    # Property Details
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, height - 120, f"Title: {prop_data['title']}")
    
    c.setFont("Helvetica", 12)
    c.drawString(40, height - 150, f"Price Range: {prop_data['price']}")
    c.drawString(40, height - 180, f"Specifications: {prop_data['details']}")
    c.drawString(40, height - 210, f"Source Web Link: {prop_data['source_link']}")
    
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(40, 40, "Generated automatically via Addon Buildmasters Bot.")
    
    c.save()
    return filename

async def download_property_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data_idx = int(query.data.split("_")[-1])
    properties = context.user_data.get('last_results', [])
    
    if properties and len(properties) > data_idx:
        prop = properties[data_idx]
        pdf_path = generate_pdf(prop)
        
        with open(pdf_path, 'rb') as f:
            await context.bot.send_document(
                chat_id=query.message.chat_id,
                document=f,
                filename=f"Property_{data_idx+1}_Details.pdf",
                caption=f"📄 Ye lijiye aapki property ki poori detail file: *{prop['title']}*",
                parse_mode="Markdown"
            )
        os.remove(pdf_path)
    else:
        await query.message.reply_text("⚠️ Session expired ya property data nahi mila. Kripya dobara search karein.")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Property search cancel kar di gayi hai.")
    return ConversationHandler.END

# --- MAIN APP ROUTER ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Conversation handler for interactive property filtering
    prop_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(property_search_start, pattern="^menu_property_search$")],
        states={
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_location)],
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_price)],
            PROPERTY_TYPE: [CallbackQueryHandler(receive_type_and_search, pattern="^type_")],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(prop_conv_handler)
    app.add_handler(CallbackQueryHandler(download_property_pdf, pattern="^download_prop_"))
    app.add_handler(CallbackQueryHandler(start, pattern="^back_to_menu$"))

    print("🤖 Bot is running smoothly...")
    app.run_polling()

if __name__ == "__main__":
    main()
