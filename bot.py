import os
import requests
import html
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ["BOT_TOKEN"]
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

# Message sent privately when someone REQUESTS to join
JOIN_REQUEST_MESSAGE = """
با سلام و درود دوست عزیز 👋
.درخواست عضویت شما در گروه ایرانیان نیوکسل دریافت شد

به منظور حفظ امنیت گروه و همچنین جلوگیری از بات های مزاحم لطفاً شماره موبایل استرالیایی خودتون رو با فونت انگلیسی برای ادمین گروه ارسال کنید تا درخواست تون بررسی بشه.
@Hamidreza_mohammadzadeh
همچنین مطمئن بشید که تنظیمات حساب تلگرامتون به‌درستی انجام شده باشه تا بتونید بدون مشکل به گروه اضافه بشید. 😊

این گروه مخصوص ایرانیان مقیم نیوکسل استرالیا میباشد 😊
باتشکر از همکاري تون
"""

# Message posted INSIDE the group after a new member joins
WELCOME_MESSAGE = """
به جمع ایرانیان نیوکسل استرالیا خوش اومدی!❤️
هدف این گروه اینه که کنار هم باشیم، از همدیگه حمایت کنیم و وقتی از خونه و عزیزانمون دوریم، زندگی رو برای هم کمی راحت‌تر و شادتر کنیم. 😊
ممنون که با احترام، انرژی مثبت و لبخندت بخشی از جمع ما هستی. 🌱
امیدوارم خیلی زود از نزدیک ببینیمت! 🙌
ارادتمند شما،
حمیدرضا
"""


def send_message(chat_id, text, parse_mode=None):
    data = {
        "chat_id": chat_id,
        "text": text
    }

    if parse_mode:
        data["parse_mode"] = parse_mode

    return requests.post(
        f"{TELEGRAM_API}/sendMessage",
        json=data,
        timeout=10
    )


@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()

    # -------------------------------------------------
    # 1. NEW JOIN REQUEST
    # Send a PRIVATE message to the person
    # -------------------------------------------------

    if "chat_join_request" in update:
        join_request = update["chat_join_request"]

        user_chat_id = join_request["user_chat_id"]

        send_message(
            user_chat_id,
            JOIN_REQUEST_MESSAGE
        )

    # -------------------------------------------------
    # 2. NEW MEMBER ACTUALLY JOINS THE GROUP
    # Send a welcome message INSIDE the group
    # -------------------------------------------------

    if "chat_member" in update:
        member_update = update["chat_member"]

        old_status = member_update["old_chat_member"]["status"]
        new_member = member_update["new_chat_member"]
        new_status = new_member["status"]

        # Only trigger when someone who was outside
        # the group becomes a member
        if old_status in ["left", "kicked"] and new_status == "member":

            user = new_member["user"]

            # Don't welcome bots
            if not user.get("is_bot", False):

                user_id = user["id"]
                first_name = html.escape(
                    user.get("first_name", "there")
                )

                group_chat_id = member_update["chat"]["id"]

                # Make the person's name clickable
                mention = (
                    f'<a href="tg://user?id={user_id}">'
                    f'{first_name}</a>'
                )

                welcome_text = WELCOME_MESSAGE.format(
                    name=mention
                )

                send_message(
                    group_chat_id,
                    welcome_text,
                    parse_mode="HTML"
                )

    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(
        host="0.0.0.0",
        port=port
    )
