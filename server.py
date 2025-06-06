import os
import flask
import requests
import main

from flask import request

TOKEN = "7150884626:AAGMo7q4Rg-o9wDxo5PwI-Cwz46ip9rBc5M"
WEBHOOK_URL = "https://ytdownloadontelegram.onrender.com"

app = flask.Flask(__name__)

def set_webhook():
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}"
    response = requests.get(url)
    return response.json()

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        if text.stratswith("https://www.youtube.com/"):
            video_url = text
            send_message(chat_id, "Download started!")
            main.download_youtube_video(video_url)
            send_message(chat_id, "Download complete!")
    return "OK"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id,"text": text})

if __name__ == "__main__":
    set_webhook()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))