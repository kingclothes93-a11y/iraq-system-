from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from jnius import autoclass
from android.permissions import request_permissions, Permission

class CoinsApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=30, spacing=20)
        self.status = Label(text="System Ready", font_size='18sp')
        
        btn_1 = Button(text="STEP 1: ACCESS", background_color=(0.2, 0.4, 0.9, 1))
        btn_2 = Button(text="STEP 2: BATTERY", background_color=(0.8, 0.5, 0.2, 1))
        btn_3 = Button(text="STEP 3: ACTIVATE", background_color=(0.1, 0.7, 0.2, 1))

        btn_1.bind(on_press=lambda x: self.open_perm("android.provider.Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION"))
        btn_2.bind(on_press=lambda x: self.open_perm("android.provider.Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS"))
        btn_3.bind(on_press=self.start_service)

        layout.add_widget(self.status); layout.add_widget(btn_1); layout.add_widget(btn_2); layout.add_widget(btn_3)
        Clock.schedule_once(lambda dt: request_permissions(["android.permission.POST_NOTIFICATIONS"]), 1)
        return layout

    def open_perm(self, action):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            Settings = autoclass('android.provider.Settings')
            activity = PythonActivity.mActivity
            intent = Intent(autoclass(action))
            if "BATTERY" in action: intent.setData(Uri.parse("package:" + activity.getPackageName()))
            activity.startActivity(intent)
        except: pass

    def start_service(self):
        try:
            from android import mActivity
            # اسم الخدمة يجب أن يكون دقيقاً جداً ليتصل بملف service.py
            service = autoclass('org.test.coinssync.ServiceMyservice')
            service.start(mActivity, "")
            self.status.text = "✅ ACTIVE"
        except Exception as e:
            self.status.text = f"❌ Error: {str(e)}"
