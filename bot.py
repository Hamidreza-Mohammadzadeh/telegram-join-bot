import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ["BOT_TOKEN"]
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

WELCOME_MESSAGE = """
سلام 👋

درخواست عضویت شما در گروه ایرانیان نیوکاسل دریافت شد

به منظور حفظ امنیت گروه و همچنین جلوگیری از بات های مزاحم لطفاً شماره موبایل استرالیایی خودتون رو برای ادمین گروه ارسال کنید تا درخواست تون بررسی بشه.
این گروه مخصوص ایرانیان مقیم نیوکسل میباشد 😊
@Hamidreza_mohammadzadeh

باتشکر از همکاري تون

"""

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()

    if "chat_join_request" in update:
        join_request = update["chat_join_request"]
        user_chat_id = join_request["user_chat_id"]

        requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": user_chat_id,
                "text": WELCOME_MESSAGE
            }
        )

    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
