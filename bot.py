import os
import json
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from google.oauth2.credentials import Credentials

# ================= Configuration =================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8712926615:AAFNK7TnmU5qEYdyukSsJiDOimmtSYJteM8")
GMB_LOCATION_ID = "17965482236175056297"  # Aapka Real Google Business Profile ID

pending_updates = {}
waiting_custom_edit = {}

GMB_SCOPES = ["https://www.googleapis.com/auth/business.manage"]

def get_gmb_token():
    if not os.path.exists("token.json"):
        raise FileNotFoundError("token.json missing! Upload it to Render Secret Files.")
    creds = Credentials.from_authorized_user_file("token.json", GMB_SCOPES)
    return creds.token

# ================= Update Profile on Google =================
def update_gmb_description(new_description):
    token = get_gmb_token()
    # Official Google Business Profile API v1 Endpoint
    url = f"https://mybusinessbusinessinformation.googleapis.com/v1/locations/{GMB_LOCATION_ID}?updateMask=profile.description"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "profile": {
            "description": new_description[:750]  # Max 750 chars allowed by Google
        }
    }
    resp = requests.patch(url, headers=headers, json=payload)
    if resp.status_code in [200, 201]:
        return True
    else:
        raise Exception(f"Google API Error: {resp.text}")

# ================= Default SEO Pack for Addon Buildmasters =================
SEO_PACK = {
    "business_name": "Addon Buildmasters Private Limited",
    "primary_category": "Construction company",
    "secondary_categories": "Interior designer, Modular home builder, Civil engineer",
    "optimized_description": (
        "Addon Buildmasters Private Limited is Dharamshala & Kangra's premier turnkey construction "
        "and luxury interior design company. We specialize in modern residential villa construction, "
        "commercial building projects, 3D architectural elevations, and custom modular kitchens across "
        "Himachal Pradesh. With earthquake-resistant engineering, premium materials, and transparent "
        "timelines, we deliver dream homes from foundation to finish. Whether you need new home construction "
        "in Dharamshala, property development in Kangra, or luxury interior renovation, our expert team "
        "provides complete end-to-end solutions. Contact Addon Buildmasters today for a free site visit and consultation!"
    )[:745],
    "services": [
        "Turnkey Home Construction (Dharamshala & Kangra)",
        "Luxury Interior Design & 3D Space Renderings",
        "Custom Modular Kitchen & Wardrobe Design",
        "Modern Architectural Front Elevation Design",
        "Commercial & Hotel Building Projects",
        "Earthquake-Resistant Structural Engineering"
    ],
    "keywords": [
        "Construction company in Dharamshala",
        "Best builders in Kangra",
        "Modular kitchen in Dharamshala",
        "Interior designers Himachal Pradesh",
        "Turnkey contractor Dharamshala"
    ]
}

# ================= Telegram Handlers =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 **Namaste Addon Buildmasters!**\n\n"
        "Main aapka **Google Profile SEO Manager** hoon.\n\n"
        "Apne Google Business Profile ka SEO dekhne aur live update karne ke liye **/seo** bhejein.",
        parse_mode="Markdown"
    )

async def seo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    desc = pending_updates.get(chat_id, SEO_PACK["optimized_description"])
    
    services_text = "\n".join([f"• {s}" for s in SEO_PACK["services"]])
    keywords_text = ", ".join([f"`{k}`" for k in SEO_PACK["keywords"]])
    
    msg = (
        f"🏢 **{SEO_PACK['business_name']}**\n"
        f"🎯 **Location ID:** `{GMB_LOCATION_ID}`\n\n"
        f"🏷️ **Primary Category:** `{SEO_PACK['primary_category']}`\n"
        f"📂 **Sub-Categories:** `{SEO_PACK['secondary_categories']}`\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🚀 **Recommended Local-SEO Description:**\n\n"
        f"{desc}\n\n"
        f"*(Length: {len(desc)} / 750 characters)*\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🛠️ **Target Services:**\n"
        f"{services_text}\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🎯 **Top Local Keywords:**\n"
        f"{keywords_text}\n\n"
        "👉 Kya aap is description ko apne Google Profile par **LIVE** update karna chahte hain?"
    )
    
    keyboard = [
        [InlineKeyboardButton("✅ Live Update on Google Profile", callback_data="apply_update")],
        [InlineKeyboardButton("✏️ Apna Custom Description Likhein", callback_data="custom_edit")]
    ]
    
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    
    if query.data == "apply_update":
        new_text = pending_updates.get(chat_id, SEO_PACK["optimized_description"])
        await query.edit_message_text("Google Business Profile par update ho raha hai... 🚀")
        try:
            update_gmb_description(new_text)
            await context.bot.send_message(
                chat_id=chat_id,
                text="🎉 **Mubarak ho!** Naya Local SEO Description aapke Google Business Profile par **LIVE** update ho gaya hai!"
            )
        except Exception as e:
            await context.bot.send_message(chat_id=chat_id, text=f"❌ Google API Error: {str(e)}")
            
    elif query.data == "custom_edit":
        waiting_custom_edit[chat_id] = True
        await query.edit_message_text(
            "✏️ **Apna naya Description likhkar message bhejein:**\n(Maximum 750 characters)"
        )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if waiting_custom_edit.get(chat_id):
        user_text = update.message.text
        waiting_custom_edit[chat_id] = False
        
        if len(user_text) > 750:
            await update.message.reply_text(f"⚠️ Text {len(user_text)} characters ka hai. Limit 750 hai. Thoda chhota karke dubara bhejein.")
            return
            
        await update.message.reply_text("Google Profile par live update ho raha hai... ⏳")
        try:
            update_gmb_description(user_text)
            pending_updates[chat_id] = user_text
            await update.message.reply_text("✅ **Successfully Updated!** Aapka custom description Google par live update ho gaya hai.")
        except Exception as e:
            await update.message.reply_text(f"❌ Update Error: {str(e)}")

# ================= Main =================
if __name__ == "__main__":
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("seo", seo_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    print("Addon Buildmasters Live SEO Bot is running...")
    app.run_polling()
