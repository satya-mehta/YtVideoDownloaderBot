import os
import flask
import requests
import main

from flask import request

TOKEN = "7150884626:AAGMo7q4Rg-o9wDxo5PwI-Cwz46ip9rBc5M"
WEBHOOK_URL = "https://ytdownloadontelegram.onrender.com"

app = flask.Flask(__name__)

def split_file(file_path, max_size=50 * 1024 * 1024):
    """
    Splits the file into chunks of size max_size and returns a list of part file paths.
    """
    parts = []
    file_size = os.path.getsize(file_path)
    if file_size <= max_size:
        # No need to split
        return [file_path]
    
    part_num = 1
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(max_size)
            if not chunk:
                break
            part_filename = f"{file_path}.part{part_num:03d}"
            with open(part_filename, "wb") as part_file:
                part_file.write(chunk)
            parts.append(part_filename)
            part_num += 1
    return parts

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
    print("Recieved data :", data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        if "youtube.com/" in text:
            video_url = text
            send_message(chat_id, "Download started!")
            file_path = main.download_youtube_video(video_url)
            send_message(chat_id, "Download complete! sending file in 3 secs...")
            if file_path:
                file_parts = split_file(file_path)
                if part.len() > 1:
                    send_message(chat_id, f"File size is larger than allowed size limit, sending files in {part.len()} parts")
                for part in file_parts:
                    send_file(chat_id, part)
            else:
                send_message(chat_id, "Unknoen error Occured")
        if text.startswith("/start"):
            send_message(chat_id, "Welcome to the bot interface.")
    return "OK"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id,"text": text})

def send_file(chat_id, file_path):
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    try:
        with open(file_path, "rb") as file:
            response = requests.post(url, data={"chat_id": chat_id}, files={"document": file})
        if response.status_code == 200:
            print(f"File sent successfully: {file_path}")
            os.remove(file_path)
            print(f"File deleted: {file_path}")
        else:
            print(f"failed to send file. status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Error sending file: {e}")

if __name__ == "__main__":
    set_webhook()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))