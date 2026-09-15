import os
import requests
from flask import Flask, request

app = Flask(__name__)

# --------------------------------------------------
# TELEGRAM SETTINGS
# --------------------------------------------------

TOKEN = os.environ["BOT_TOKEN"]
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"


# --------------------------------------------------
# MESSAGE 1
# Sent privately BEFORE joining the group
# --------------------------------------------------

JOIN_REQUEST_MESSAGE = """
با سلام و درود دوست عزیز 👋
درخواست عضویت شما در گروه ایرانیان نیوکسل دریافت شد.

به منظور حفظ امنیت گروه و همچنین جلوگیری از بات‌های مزاحم لطفاً شماره موبایل استرالیایی خودتون رو با فونت انگلیسی برای ادمین گروه ارسال کنید تا درخواست‌تون بررسی بشه.
@Hamidreza_mohammadzadeh
همچنین مطمئن بشید که تنظیمات حساب تلگرامتون به‌درستی انجام شده باشه تا بتونیم شما رو بدون مشکل به گروه اضافه کنیم😊
این گروه مخصوص ایرانیان مقیم نیوکسل استرالیا می‌باشد 😊

با تشکر از همکاری‌تون
"""


# --------------------------------------------------
# MESSAGE 2
# Sent privately AFTER joining the group
# --------------------------------------------------

WELCOME_MESSAGE = """
{name} عزیز،
به جمع ایرانیان نیوکسل استرالیا خوش اومدی! ❤️
هدف این گروه اینه که کنار هم باشیم، از همدیگه حمایت کنیم و وقتی از خونه و عزیزانمون دوریم، زندگی رو برای هم کمی راحت‌تر و شادتر کنیم. 😊
ممنون که با احترام، انرژی مثبت و لبخندت بخشی از جمع ما هستی. 🌱
امیدوارم خیلی زود از نزدیک ببینیمت! 🙌
ارادتمند شما،
حمیدرضا
"""


# --------------------------------------------------
# SEND TELEGRAM MESSAGE
# --------------------------------------------------

def send_message(chat_id, text):
    try:
        response = requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text
            },
            timeout=10
        )

        # Show errors in Render logs if sending fails
        if not response.ok:
            print(
                "Telegram sendMessage error:",
                response.status_code,
                response.text
            )

        return response

    except Exception as error:
        print("Error sending Telegram message:", error)
        return None


# --------------------------------------------------
# RENDER HOME PAGE
# --------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"


# --------------------------------------------------
# TELEGRAM WEBHOOK
# --------------------------------------------------

@app.route("/webhook", methods=["POST"])
def webhook():

    update = request.get_json(silent=True)

    if not update:
        return "OK", 200


    # ==================================================
    # 1. USER SENDS A JOIN REQUEST
    # ==================================================

    if "chat_join_request" in update:

        join_request = update["chat_join_request"]

        user_chat_id = join_request["user_chat_id"]

        user = join_request["from"]

        first_name = user.get("first_name", "دوست عزیز")

        print(
            f"New join request from: "
            f"{first_name} - Telegram ID: {user.get('id')}"
        )

        # Send first message PRIVATELY
        send_message(
            user_chat_id,
            JOIN_REQUEST_MESSAGE
        )


    # ==================================================
    # 2. USER ACTUALLY JOINS THE GROUP
    # ==================================================

    if "chat_member" in update:

        member_update = update["chat_member"]

        old_member = member_update["old_chat_member"]
        new_member = member_update["new_chat_member"]

        old_status = old_member["status"]
        new_status = new_member["status"]

        # Only trigger when someone outside the group
        # becomes a new member
        if (
            old_status in ["left", "kicked"]
            and new_status == "member"
        ):

            user = new_member["user"]

            # Ignore bots
            if not user.get("is_bot", False):

                user_id = user["id"]

                first_name = user.get(
                    "first_name",
                    "دوست عزیز"
                )

                print(
                    f"New member joined: "
                    f"{first_name} - Telegram ID: {user_id}"
                )

                welcome_text = WELCOME_MESSAGE.format(
                    name=first_name
                )

                # Send welcome message ONLY to
                # the new member's PRIVATE chat
                send_message(
                    user_id,
                    welcome_text
                )


    return "OK", 200


# --------------------------------------------------
# LOCAL / RENDER SERVER
# --------------------------------------------------

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
