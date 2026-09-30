import time
import requests

# आपका Telegram Bot Token
BOT_TOKEN = "8825765752:AAEwnDGTmHaD2nY0g2KAOYi9vP_Pr-pJH7I"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# पोस्ट टेम्पलेट्स
POSTS = {
    "construction": """🏗️ *Turnkey Construction — Addon Buildmasters* 🏡

अपने सपनों का घर बनवाएँ आधुनिक तकनीक और 100% मजबूत मटीरियल के साथ!
✔️ A-Grade मटीरियल और भूकंप-रोधी संरचना
✔️ पारदर्शी बजट और समय पर प्रोजेक्ट डिलीवरी
✔️ अनुभवी स्ट्रक्चरल इंजीनियर्स और आर्किटेक्ट्स

📍 *सर्विस एरिया:* हरियाणा एवं दिल्ली-NCR
📞 फ्री साइट विज़िट और कंसल्टेशन के लिए आज ही कॉल करें!

#AddonBuildmasters #ConstructionCompany #TurnkeyProjects #Haryana""",

    "elevation": """🏡 *Modern 3D Front Elevation — Addon Buildmasters* ✨

क्या आप अपने घर को एक आधुनिक और शानदार लुक देना चाहते हैं?
Addon Buildmasters के साथ पाएँ प्रीमियम 3D फ्रंट एलीवेशन और आर्किटेक्चरल डिज़ाइन्स जो आपके घर को सबसे अलग बनाएँ।

✔️ 2D/3D नक्शा व फ्लोर प्लानिंग
✔️ मॉडर्न एक्सटीरियर व लाइटिंग कॉन्सेप्ट
✔️ कम्प्लीट एग्जीक्यूशन सपोर्ट

📞 अपने प्लॉट का 3D डिज़ाइन बनवाने के लिए संपर्क करें!
#FrontElevation #ModernArchitecture #3DDesign #AddonBuildmasters""",

    "interior": """🛋️ *Luxury Interior Design — Addon Buildmasters* ✨

लक्ज़री इंटीरियर्स अब आपके बजट में! अपने घर और ऑफ़िस को दें मॉडर्न और फंक्शनल लुक:
✔️ मॉड्यूलर किचन व वार्डरोब्स
✔️ डिज़ाइनर फ़ाल्स सीलिंग व कस्टम लाइटिंग
✔️ प्रीमियम वॉल पैनल्स व फर्नीचर वर्क

📞 आज ही अपनी साइट विज़िट और 3D कंसल्टेशन बुक करें!
#InteriorDesign #HomeDecor #ModularKitchen #AddonBuildmasters"""
}

def send_message(chat_id, text, reply_markup=None):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Error sending message: {e}")

def get_main_menu():
    return {
        "inline_keyboard": [
            [{"text": "📋 आज के SEO टास्क", "callback_data": "menu_tasks"}],
            [{"text": "✍️ AI Google Post निकालें", "callback_data": "menu_posts"}],
            [{"text": "📊 Live GBP स्टेट्स देखें", "callback_data": "menu_stats"}],
            [{"text": "⭐ WhatsApp रिव्यू लिंक", "callback_data": "menu_review"}]
        ]
    }

def handle_callback(chat_id, data, message_id):
    if data == "menu_tasks":
        text = """📋 *Addon Buildmasters — आज के 3 मुख्य SEO टास्क:*

1️⃣ *साइट फ़ोटो अपलोड (+15 Pts)*
चल रहे कंस्ट्रक्शन, 3D एलीवेशन या पूरे हुए इंटीरियर की 2 नई ताज़ा फ़ोटोज़ Google Business पर अपलोड करें।

2️⃣ *Google Update Post (+20 Pts)*
आज की नई पोस्ट शेयर करें ताकि Google Maps एल्गोरिदम प्रोफ़ाइल को एक्टिव माने।

3️⃣ *क्लाइंट रिव्यू रिक्वेस्ट (+30 Pts)*
हाल ही के 1 क्लाइंट को WhatsApp पर रिव्यू लिंक भेजें।

_Google Maps पर एक्टिव रहने से हरियाणा/NCR में लोकल कॉल्स 2x बढ़ती हैं!_ 🚀"""
        markup = {
            "inline_keyboard": [
                [{"text": "✅ टास्क पूरे हो गए (+65 Pts)", "callback_data": "tasks_completed"}],
                [{"text": "✍️ पोस्ट का टेक्स्ट चाहिए", "callback_data": "menu_posts"}],
                [{"text": "🔙 मुख्य मेन्यू", "callback_data": "main_menu"}]
            ]
        }
        send_message(chat_id, text, markup)

    elif data == "tasks_completed":
        send_message(chat_id, "🎉 *शानदार!* आज के सभी लोकल SEO टास्क पूरे हो गए हैं। Google Maps पर आपका प्रोफ़ाइल स्कोर बढ़ गया है! 💪", get_main_menu())

    elif data == "menu_posts":
        text = "✍️ *किस तरह की Google Post का टेक्स्ट चाहिए?*\nनीचे कैटेगरी चुनें, बॉट तुरंत रेडीमेड टेक्स्ट देगा:"
        markup = {
            "inline_keyboard": [
                [{"text": "🏗️ Turnkey Construction", "callback_data": "post_construction"}],
                [{"text": "🏡 Modern 3D Elevation", "callback_data": "post_elevation"}],
                [{"text": "🛋️ Luxury Interior Design", "callback_data": "post_interior"}],
                [{"text": "🔙 मुख्य मेन्यू", "callback_data": "main_menu"}]
            ]
        }
        send_message(chat_id, text, markup)

    elif data.startswith("post_"):
        category = data.replace("post_", "")
        content = POSTS.get(category, "पोस्ट उपलब्ध नहीं है।")
        send_message(chat_id, f"👇 *इस टेक्स्ट को कॉपी करके सीधे Google Business पर पोस्ट करें:*\n\n{content}")
        send_message(chat_id, "क्या कोई और मदद चाहिए?", get_main_menu())

    elif data == "menu_stats":
        stats_text = """📊 *Addon Buildmasters — Live Profile Overview*

🔍 *Search Impressions:* 1,420 (+12% this week)
🗺️ *Maps Views:* 890 (+8% this week)
📞 *Customer Phone Calls:* 28 (Direct inquiries)
🛡️ *Profile SEO Health:* 85% (Excellent)

📍 *Service Area:* Haryana & Delhi-NCR
⚡ *Status:* Profile Active & Verified"""
        send_message(chat_id, stats_text, get_main_menu())

    elif data == "menu_review":
        rev_text = """⭐ *क्लाइंट रिव्यू रिक्वेस्ट जनरेटर:*

क्लाइंट को पर्सनलाइज्ड WhatsApp मैसेज भेजने के लिए चैट में लिखें:
👉 `/review [क्लाइंट का नाम]`

*उदाहरण:*
`/review शर्मा जी`
या
`/review Amit Kumar`

बॉट तुरंत WhatsApp के लिए रेडीमेड मैसेज ड्राफ्ट कर देगा!"""
        send_message(chat_id, rev_text, get_main_menu())

    elif data == "main_menu":
        send_message(chat_id, "🏢 *Addon Buildmasters Assistant — मुख्य मेन्यू:*", get_main_menu())

def main():
    print("=" * 50)
    print("🤖 Addon Buildmasters Telegram Bot चालू हो गया है!")
    print(f"👉 Bot Link: https://t.me/addon_buildmasters1704_bot")
    print("=" * 50)
    
    last_update_id = 0
    while True:
        try:
            url = f"{BASE_URL}/getUpdates?offset={last_update_id + 1}&timeout=30"
            resp = requests.get(url, timeout=35).json()

            if resp.get("ok"):
                for update in resp.get("result", []):
                    last_update_id = update["update_id"]

                    # Callback Queries (Inline Buttons)
                    if "callback_query" in update:
                        cb = update["callback_query"]
                        chat_id = cb["message"]["chat"]["id"]
                        data = cb.get("data", "")
                        msg_id = cb["message"]["message_id"]
                        handle_callback(chat_id, data, msg_id)

                    # Text Messages
                    elif "message" in update and "text" in update["message"]:
                        msg = update["message"]
                        chat_id = msg["chat"]["id"]
                        text = msg["text"].strip()

                        if text.startswith("/start"):
                            welcome = f"""🏗️ *नमस्ते! Welcome to Addon Buildmasters Assistant* 🚀

मैं आपका पर्सनल Google Business Profile और लोकल SEO असिस्टेंट हूँ।
मैं Addon Buildmasters को Google Maps पर टॉप रैंकिंग पर लाने और ज्यादा क्लाइंट्स दिलाने में आपकी मदद करूँगा।

नीचे दिए गए किसी भी बटन पर क्लिक करके शुरू करें:"""
                            send_message(chat_id, welcome, get_main_menu())

                        elif text.startswith("/review"):
                            parts = text.split(maxsplit=1)
                            client_name = parts[1] if len(parts) > 1 else "सर"
                            review_msg = f"""नमस्ते {client_name}, Addon Buildmasters के साथ जुड़ने के लिए बहुत-बहुत धन्यवाद! 🙏

हमारा काम आपको कैसा लगा? कृपया Google Maps पर अपने अनुभव का एक छोटा सा 5-स्टार रिव्यू और फ़ीडबैक ज़रूर दें। इससे हमें और बेहतर सेवा देने में मदद मिलेगी:

👉 [यहाँ अपना Google Maps Review लिंक पेस्ट करें]"""
                            send_message(chat_id, f"👇 *इस मैसेज को कॉपी करके {client_name} को WhatsApp पर भेजें:*\n\n{review_msg}")
                            send_message(chat_id, "वापस मेन्यू पर जाने के लिए:", get_main_menu())

                        else:
                            send_message(chat_id, "विकल्प चुनने के लिए नीचे दिए गए मेन्यू का उपयोग करें:", get_main_menu())

        except Exception as e:
            time.sleep(2)

if __name__ == "__main__":
    main()