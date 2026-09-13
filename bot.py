{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4cd52e52-3819-49f9-a81c-e56986dd9c04",
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import requests\n",
    "from flask import Flask, request\n",
    "\n",
    "app = Flask(__name__)\n",
    "\n",
    "TOKEN = os.environ[\"BOT_TOKEN\"]\n",
    "TELEGRAM_API = f\"https://api.telegram.org/bot{TOKEN}\"\n",
    "\n",
    "WELCOME_MESSAGE = \"\"\"\n",
    "با درود خدمت شما دوست گرانقدر 👋\n",
    "درخواست عضویت شما در گروه ایرانیان نیوکاسل دریافت شد. 🇮🇷🇦🇺\n",
    "\n",
    "به منظور حفظ امنیت گروه و همچنین جلوگیری از بات های مزاحم لطفاً شماره موبایل استرالیایی خودتون رو برای ادمین گروه ارسال کنید تا درخواست تون بررسی بشه.\n",
    "این گروه مخصوص ایرانیان مقیم نیوکسل میباشد\n",
    "\n",
    "ممنون از همکاری تون 🌹\n",
    "حمیدرضا\n",
    "گروه ایرانیان نیوکسل استرالیا\n",
    "\"\"\"\n",
    "\n",
    "\n",
    "@app.route(\"/\", methods=[\"GET\"])\n",
    "def home():\n",
    "    return \"Bot is running!\"\n",
    "\n",
    "\n",
    "@app.route(\"/webhook\", methods=[\"POST\"])\n",
    "def webhook():\n",
    "    update = request.get_json()\n",
    "\n",
    "    if \"chat_join_request\" in update:\n",
    "        join_request = update[\"chat_join_request\"]\n",
    "\n",
    "        user_chat_id = join_request[\"user_chat_id\"]\n",
    "\n",
    "        requests.post(\n",
    "            f\"{TELEGRAM_API}/sendMessage\",\n",
    "            json={\n",
    "                \"chat_id\": user_chat_id,\n",
    "                \"text\": WELCOME_MESSAGE\n",
    "            }\n",
    "        )\n",
    "\n",
    "    return \"OK\", 200\n",
    "\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    port = int(os.environ.get(\"PORT\", 10000))\n",
    "    app.run(host=\"0.0.0.0\", port=port)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
