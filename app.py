from flask import Flask, send_from_directory
import os
import threading

app = Flask(__name__)

# Static folder for AI generated images
os.makedirs("static", exist_ok=True)

@app.route("/")
def home():
    return "🤖 Addon Buildmasters Telegram Bot is Running 24/7 Live!"

@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)

def start_bot():
    print("🚀 Starting Telegram Bot in Background...")
    os.system("python bot.py")

if __name__ == "__main__":
    # Background thread mein bot.py chalega
    t = threading.Thread(target=start_bot)
    t.daemon = True
    t.start()

    # Render ke liye Flask web server chalega
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
