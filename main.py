import os
import random
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.core.text import LabelBase

# ===== الخط العربي =====
ARABIC_FONT = "Roboto"

try:
    font_path = os.path.join(os.getcwd(), "cairo.ttf")
    if os.path.exists(font_path):
        LabelBase.register(name="Arabic", fn_regular=font_path)
        ARABIC_FONT = "Arabic"
except:
    pass


# ===== شاشة البداية =====
class SplashScreen(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)

        layout = BoxLayout()
        bg = Image(source="bg_lock.jpg", allow_stretch=True, keep_ratio=False)
        layout.add_widget(bg)
        self.add_widget(layout)

        from kivy.clock import Clock
        Clock.schedule_once(self.next, 2)

    def next(self, dt):
        self.manager.current = "main"


# ===== الشاشة الرئيسية =====
class MainScreen(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)

        layout = BoxLayout(orientation="vertical")

        # صورة خلفية
        bg = Image(source="bg_main.jpg", allow_stretch=True, keep_ratio=False)
        layout.add_widget(bg)

        # نص
        self.label = MDLabel(
            text="مرحبا بك 👑",
            halign="center",
            font_name=ARABIC_FONT
        )

        # إدخال
        self.input = TextInput(
            hint_text="اكتب هنا...",
            size_hint=(1, None),
            height=50,
            font_name=ARABIC_FONT
        )

        # زر
        btn = MDRaisedButton(
            text="إرسال",
            pos_hint={"center_x": 0.5},
            on_release=self.send
        )

        layout.add_widget(self.label)
        layout.add_widget(self.input)
        layout.add_widget(btn)

        self.add_widget(layout)

    def send(self, *args):
        text = self.input.text.strip()
        if text:
            self.label.text = f"👤 {text}"
            self.input.text = ""


# ===== التطبيق =====
class MainApp(MDApp):
    def build(self):
        sm = MDScreenManager()
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(MainScreen(name="main"))
        sm.current = "splash"
        return sm


if __name__ == "__main__":
    MainApp().run()
