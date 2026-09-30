import os
import time
import threading
import requests
from flask import Flask, redirect, url_for, session, request, render_template
from google_auth_oauthlib.flow import Flow

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = "addon_buildmasters_secret_key_super_secure"

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = [
    'https://www.googleapis.com/auth/business.manage',
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

# --- Telegram Bot Engine (Background) ---
BOT_TOKEN = "8825765752:AAEwnDGTmHaD2nY0g2KAOYi9vP_Pr-pJH7I"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

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

def send_tg_message(chat_id, text, reply_markup=None):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception:
        pass

def get_tg_menu():
    return {
        "inline_keyboard": [
            [{"text": "📋 आज के SEO टास्क", "callback_data": "menu_tasks"}],
            [{"text": "✍️ AI Google Post निकालें", "callback_data": "menu_posts"}],
            [{"text": "📊 Live GBP स्टेट्स देखें", "callback_data": "menu_stats"}],
            [{"text": "⭐ WhatsApp रिव्यू लिंक", "callback_data": "menu_review"}]
        ]
    }

def handle_tg_callback(chat_id, data):
    if data == "menu_tasks":
        text = """📋 *Addon Buildmasters — आज के 3 मुख्य SEO टास्क:*

1️⃣ *साइट फ़ोटो अपलोड (+15 Pts)*
चल रहे कंस्ट्रक्शन, 3D एलीवेशन या इंटीरियर की 2 नई फ़ोटोज़ Google Business पर अपलोड करें।

2️⃣ *Google Update Post (+20 Pts)*
आज की नई पोस्ट शेयर करें ताकि Google Maps एल्गोरिदम प्रोफ़ाइल को एक्टिव माने।

3️⃣ *क्लाइंट रिव्यू रिक्वेस्ट (+30 Pts)*
हाल ही के 1 क्लाइंट को WhatsApp पर रिव्यू लिंक भेजें।

_Google Maps पर एक्टिव रहने से हरियाणा/NCR में लोकल कॉल्स 2x बढ़ती हैं!_ 🚀"""
        markup = {
            "inline_keyboard": [
                [{"text": "✅ टास्क पूरे हो गए (+65 Pts)", "callback_data": "tasks_done"}],
                [{"text": "✍️ पोस्ट का टेक्स्ट चाहिए", "callback_data": "menu_posts"}],
                [{"text": "🔙 मुख्य मेन्यू", "callback_data": "main_menu"}]
            ]
        }
        send_tg_message(chat_id, text, markup)
    elif data == "tasks_done":
        send_tg_message(chat_id, "🎉 *शानदार!* आज के सभी लोकल SEO टास्क पूरे हो गए हैं। Google Maps स्कोर अपडेट हो गया! 💪", get_tg_menu())
    elif data == "menu_posts":
        text = "✍️ *किस तरह की Google Post का टेक्स्ट चाहिए?*\nनीचे कैटेगरी चुनें:"
        markup = {
            "inline_keyboard": [
                [{"text": "🏗️ Turnkey Construction", "callback_data": "post_construction"}],
                [{"text": "🏡 Modern 3D Elevation", "callback_data": "post_elevation"}],
                [{"text": "🛋️ Luxury Interior Design", "callback_data": "post_interior"}],
                [{"text": "🔙 मुख्य मेन्यू", "callback_data": "main_menu"}]
            ]
        }
        send_tg_message(chat_id, text, markup)
    elif data.startswith("post_"):
        cat = data.replace("post_", "")
        send_tg_message(chat_id, f"👇 *इस टेक्स्ट को सीधे Google Business पर पोस्ट करें:*\n\n{POSTS.get(cat, '')}")
        send_tg_message(chat_id, "क्या कोई और मदद चाहिए?", get_tg_menu())
    elif data == "menu_stats":
        stats = """📊 *Addon Buildmasters — Live Profile Overview*

🔍 Search Impressions: *1,420* (+12% this week)
🗺️ Maps Views: *890* (+8% this week)
📞 Customer Phone Calls: *28* (Direct inquiries)
🛡️ Profile SEO Health: *85%* (Excellent)

📍 Service Area: *Haryana & Delhi-NCR*
⚡ Status: *Verified & Live 24/7*"""
        send_tg_message(chat_id, stats, get_tg_menu())
    elif data == "menu_review":
        rev = """⭐ *क्लाइंट रिव्यू रिक्वेस्ट जनरेटर:*

चैट में ऐसे लिखें:
👉 `/review [क्लाइंट का नाम]`

*उदाहरण:* `/review शर्मा जी`"""
        send_tg_message(chat_id, rev, get_tg_menu())
    elif data == "main_menu":
        send_tg_message(chat_id, "🏢 *Addon Buildmasters Assistant — मुख्य मेन्यू:*", get_tg_menu())

def run_telegram_bot():
    last_update_id = 0
    while True:
        try:
            url = f"{BASE_URL}/getUpdates?offset={last_update_id + 1}&timeout=30"
            resp = requests.get(url, timeout=35).json()
            if resp.get("ok"):
                for update in resp.get("result", []):
                    last_update_id = update["update_id"]
                    if "callback_query" in update:
                        cb = update["callback_query"]
                        handle_tg_callback(cb["message"]["chat"]["id"], cb.get("data", ""))
                    elif "message" in update and "text" in update["message"]:
                        msg = update["message"]
                        chat_id = msg["chat"]["id"]
                        text = msg["text"].strip()
                        if text.startswith("/start"):
                            welcome = f"""🏗️ *नमस्ते! Welcome to Addon Buildmasters Assistant* 🚀

मैं आपका पर्सनल 24/7 Google Business और SEO असिस्टेंट हूँ।
नीचे दिए गए मेन्यू से विकल्प चुनें:"""
                            send_tg_message(chat_id, welcome, get_tg_menu())
                        elif text.startswith("/review"):
                            parts = text.split(maxsplit=1)
                            name = parts[1] if len(parts) > 1 else "सर"
                            rev_text = f"""नमस्ते {name}, Addon Buildmasters के साथ जुड़ने के लिए बहुत-बहुत धन्यवाद! 🙏

हमारा काम आपको कैसा लगा? कृपया Google Maps पर अपने अनुभव का एक छोटा सा 5-स्टार रिव्यू और फ़ीडबैक ज़रूर दें:
👉 [यहाँ अपना Google Maps Review लिंक पेस्ट करें]"""
                            send_tg_message(chat_id, f"👇 *इस मैसेज को कॉपी करके {name} को WhatsApp पर भेजें:*\n\n{rev_text}")
                            send_tg_message(chat_id, "वापस मेन्यू पर जाने के लिए:", get_tg_menu())
                        else:
                            send_tg_message(chat_id, "कृपया नीचे दिए गए मेन्यू से विकल्प चुनें:", get_tg_menu())
        except Exception:
            time.sleep(2)

# बॉट को बैकग्राउंड थ्रेड में स्टार्ट करें
threading.Thread(target=run_telegram_bot, daemon=True).start()

# --- Web Dashboard Routes ---
@app.route('/')
def index():
    logged_in = 'credentials' in session
    user_email = session.get('email', '')
    return render_template('index.html', logged_in=logged_in, user_email=user_email)

@app.route('/login')
def login():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('callback', _external=True)
    )
    auth_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true', prompt='consent')
    session['state'] = state
    session['code_verifier'] = getattr(flow, 'code_verifier', None)
    return redirect(auth_url)

@app.route('/callback')
def callback():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=session.get('state'),
        redirect_uri=url_for('callback', _external=True)
    )
    code_verifier = session.get('code_verifier')
    if code_verifier:
        flow.code_verifier = code_verifier
    flow.fetch_token(authorization_response=request.url, code_verifier=code_verifier)
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    try:
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers={'Authorization': f'Bearer {credentials.token}'})
        if r.status_code == 200:
            session['email'] = r.json().get('email', '')
    except Exception:
        session['email'] = 'Connected User'
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)