import os
import json
import io
import time
import base64
import requests
import urllib.parse
from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Google My Business Authentication
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# ================= Configuration =================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8712926615:AAFNK7TnmU5qEYdyukSsJiDOimmtSYJteM8")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "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")
OWNER_CHAT_ID = int(os.getenv("OWNER_CHAT_ID", "123456789"))  # Apna numeric Telegram ID dalein
GMB_LOCATION_ID = os.getenv("GMB_LOCATION_ID", "accounts/ACCOUNT_ID/locations/LOCATION_ID")
RENDER_BASE_URL = os.getenv("RENDER_BASE_URL", "https://addon-buildmasters-app.onrender.com")

# Temporary sessions: {chat_id: {"topic": "", "draft": "", "media_url": "", "waiting_photo": False}}
user_sessions = {}
os.makedirs("static", exist_ok=True)

# ================= GMB Authentication =================
GMB_SCOPES = ["https://www.googleapis.com/auth/business.manage"]

def get_gmb_token():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", GMB_SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                raise FileNotFoundError("credentials.json missing! Google Cloud Console se download karein.")
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", GMB_SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds.token

# ================= Publish to GMB =================
async def publish_to_gmb(content, media_url=None):
    token = get_gmb_token()
    url = f"https://mybusiness.googleapis.com/v4/{GMB_LOCATION_ID}/localPosts"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "languageCode": "en-IN",
        "summary": content,
        "callToAction": {"actionType": "CALL"}
    }
    if media_url:
        payload["media"] = [{"mediaFormat": "PHOTO", "sourceUrl": media_url}]
        
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code in [200, 201]:
        return response.json().get("name")
    else:
        raise Exception(f"GMB Error: {response.text}")

# ================= OpenRouter AI Generation =================
async def generate_post_text(topic, image_bytes=None, user_caption=None):
    prompt_text = f"""
    You are the AI manager for Addon Buildmasters Private Limited in Dharamshala, Kangra (HP).
    Write an engaging, trustworthy, local-SEO friendly Google Business Profile post about: {topic}.
    {f"User note/caption: {user_caption}" if user_caption else ""}
    Rules:
    - Tone: Professional, authoritative, and friendly for local clients.
    - Mention: Dharamshala, Kangra, Himachal Pradesh.
    - Use relevant emojis.
    - Call to Action: Invite calls or visits for free site consultation.
    - Maximum 1000 characters.
    """
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    if image_bytes:
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    }
                ]
            }
        ]
    else:
        messages = [{"role": "user", "content": prompt_text}]
        
    payload = {
        "model": "google/gemini-2.0-flash-001",
        "messages": messages
    }
    
    resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=35)
    data = resp.json()
    if "choices" in data and len(data["choices"]) > 0:
        return data["choices"][0]["message"]["content"]
    else:
        raise Exception(f"OpenRouter Error: {data}")

# ================= AI Image Generator =================
async def generate_ai_image(topic, chat_id):
    clean_topic = topic.replace("_", " ")
    image_prompt = (
        f"Ultra realistic 8k photorealistic architectural rendering of {clean_topic} "
        f"by Addon Buildmasters, luxury modern villa in Dharamshala Himachal Pradesh mountains, "
        f"clear blue sky, professional photography, cinematic lighting"
    )
    encoded = urllib.parse.quote(image_prompt)
    image_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=768&nologo=true&seed={int(time.time())}"
    
    resp = requests.get(image_url, timeout=30)
    if resp.status_code == 200:
        filename = f"ai_{chat_id}_{int(time.time())}.jpg"
        filepath = os.path.join("static", filename)
        with open(filepath, "wb") as f:
            f.write(resp.content)
        public_url = f"{RENDER_BASE_URL}/static/{filename}"
        return public_url, filepath
    else:
        raise Exception("AI image generation failed. Please try again.")

# ================= Telegram Commands & Handlers =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await update.message.reply_text(
        f"👋 **Namaste Addon Buildmasters!**\n\n"
        f"Aapka Chat ID: `{chat_id}`\n\n"
        "Nayi post banane ke liye **/newpost** likhein ya direct site ki **photo** bhej dein.",
        parse_mode="Markdown"
    )

async def new_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🏢 Property Dealing", callback_data="top_property")],
        [InlineKeyboardButton("🏗️ Construction Projects", callback_data="top_construction")],
        [InlineKeyboardButton("🛋️ Modular Kitchen & Interior", callback_data="top_interior")]
    ]
    await update.message.reply_text(
        "📌 **Kis topic par post banani hai?**",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id

    # Topic Selection
    if query.data.startswith("top_"):
        topic = query.data.replace("top_", "").capitalize()
        user_sessions[chat_id] = {"topic": topic, "waiting_photo": False}
        
        keyboard = [
            [InlineKeyboardButton("📸 1. Main Apni Photo Bhejunga", callback_data="img_manual")],
            [InlineKeyboardButton("🎨 2. AI Image Banayega", callback_data="img_ai")],
            [InlineKeyboardButton("📝 3. Sirf Text (Bina Photo)", callback_data="img_none")]
        ]
        await query.edit_message_text(
            f"Topic: **{topic}**\n\nAb image ke liye option chunein:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    # Option 1: Manual Photo Upload
    elif query.data == "img_manual":
        user_sessions[chat_id]["waiting_photo"] = True
        await query.edit_message_text(
            "📸 **Kripya abhi project ya site ki photo send karein.**\n(Aap chahein toh caption bhi likh sakte hain)."
        )

    # Option 2: AI Generated Image
    elif query.data == "img_ai":
        topic = user_sessions.get(chat_id, {}).get("topic", "Construction")
        await query.edit_message_text("🎨 **OpenRouter AI image aur post taiyar kar raha hai...** ⏳")
        
        try:
            img_public_url, local_file = await generate_ai_image(topic, chat_id)
            post_text = await generate_post_text(topic)
            
            user_sessions[chat_id]["draft"] = post_text
            user_sessions[chat_id]["media_url"] = img_public_url
            
            keyboard = [
                [InlineKeyboardButton("✅ Approve & Post to Google", callback_data="approve_post")],
                [InlineKeyboardButton("❌ Reject", callback_data="reject_post")]
            ]
            
            with open(local_file, "rb") as f:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=f,
                    caption=f"**OpenRouter AI Draft:**\n\n{post_text}",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode="Markdown"
                )
        except Exception as e:
            await context.bot.send_message(chat_id=chat_id, text=f"❌ Error: {str(e)}")

    # Option 3: Text Only
    elif query.data == "img_none":
        topic = user_sessions.get(chat_id, {}).get("topic", "Construction")
        await query.edit_message_text("✍️ OpenRouter post draft kar raha hai... ⏳")
        try:
            draft = await generate_post_text(topic)
            user_sessions[chat_id]["draft"] = draft
            user_sessions[chat_id]["media_url"] = None
            
            keyboard = [
                [InlineKeyboardButton("✅ Approve & Post to Google", callback_data="approve_post")],
                [InlineKeyboardButton("❌ Reject", callback_data="reject_post")]
            ]
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"**OpenRouter Draft:**\n\n{draft}",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown"
            )
        except Exception as e:
            await context.bot.send_message(chat_id=chat_id, text=f"❌ Error: {str(e)}")

    # Approve & Post to Google My Business
    elif query.data == "approve_post":
        data = user_sessions.get(chat_id)
        if data and data.get("draft"):
            if query.message.photo:
                await query.edit_message_caption(caption="Publishing live on Google My Business... 🚀")
            else:
                await query.edit_message_text("Publishing live on Google... 🚀")
            try:
                post_id = await publish_to_gmb(data["draft"], data.get("media_url"))
                success_msg = f"✅ Post successfully Google My Business par LIVE ho gayi!\nPost ID: `{post_id}`"
                await context.bot.send_message(chat_id=chat_id, text=success_msg, parse_mode="Markdown")
            except Exception as e:
                await context.bot.send_message(chat_id=chat_id, text=f"❌ Google API Error: {str(e)}")
            user_sessions.pop(chat_id, None)

    # Reject Post
    elif query.data == "reject_post":
        await context.bot.send_message(chat_id=chat_id, text="Post cancel kar di gayi hai. Nayi post ke liye /newpost bhejein.")
        user_sessions.pop(chat_id, None)

# ================= Photo Upload Handler (AI Vision) =================
async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await update.message.reply_text("📸 Photo OpenRouter AI analyze kar raha hai aur post draft ho raha hai... ⏳")
    
    try:
        photo_file = await update.message.photo[-1].get_file()
        file_bytes = await photo_file.download_as_bytearray()
        
        caption = update.message.caption or "Site project photo"
        topic = user_sessions.get(chat_id, {}).get("topic", "Construction & Design")
        
        draft = await generate_post_text(topic, image_bytes=file_bytes, user_caption=caption)
        
        user_sessions[chat_id] = {
            "topic": topic,
            "draft": draft,
            "media_url": photo_file.file_path
        }
        
        keyboard = [
            [InlineKeyboardButton("✅ Approve & Post with Photo", callback_data="approve_post")],
            [InlineKeyboardButton("❌ Reject", callback_data="reject_post")]
        ]
        
        await update.message.reply_text(
            f"**Aapki Photo ke sath OpenRouter AI Draft:**\n\n{draft}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# ================= Main Runner =================
if __name__ == "__main__":
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("newpost", new_post))
    app.add_handler(CommandHandler("trial", new_post))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    
    print("Addon Buildmasters Bot running with OpenRouter...")
    app.run_polling()
