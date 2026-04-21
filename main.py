from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

# ===== شاشة كلمة السر =====
class LockScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        bg = AsyncImage(
            source="https://w0.peakpx.com/wallpaper/404/695/HD-wallpaper-sung-jin-woo-eye-glowing-blue-anime-solo-leveling.jpg",
            allow_stretch=True, keep_ratio=False, size_hint=(1, 1)
        )
        overlay = Widget()
        with overlay.canvas:
            Color(0, 0, 0, 0.5)
            self.rect = Rectangle(size=(2000, 4000))
        
        title = MDLabel(
            text="SHADOW MONARCH", halign="center", theme_text_color="Custom",
            text_color=(0, 0.8, 1, 1), font_style="H5", bold=True, pos_hint={"center_y": 0.8}
        )
        self.password = TextInput(
            password=True, size_hint=(0.7, 0.06), pos_hint={"center_x": 0.5, "center_y": 0.5},
            background_color=(0, 0, 0, 0.8), foreground_color=(0, 0.8, 1, 1)
        )
        btn = MDRaisedButton(
            text="ARISES", pos_hint={"center_x": 0.5, "center_y": 0.35},
            on_release=self.check
        )
        layout.add_widget(bg); layout.add_widget(overlay); layout.add_widget(title)
        layout.add_widget(self.password); layout.add_widget(btn)
        self.add_widget(layout)

    def check(self, *args):
        if self.password.text == "20057": self.manager.current = "main"

# ===== الشاشة الرئيسية =====
class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        top = FloatLayout(size_hint_y=0.4)
        img = AsyncImage(source="https://w0.peakpx.com/wallpaper/326/289/HD-wallpaper-sung-jin-woo-solo-leveling-anime-aesthetic-shadows.jpg", allow_stretch=True, keep_ratio=False)
        lbl = MDLabel(text="[SYSTEM]: Welcome King Mustafa", halign="center", theme_text_color="Custom", text_color=(0, 0.8, 1, 1), pos_hint={"center_y": 0.2})
        top.add_widget(img); top.add_widget(lbl)
        
        self.scroll = ScrollView(); self.msgs = BoxLayout(orientation='vertical', size_hint_y=None); self.msgs.bind(minimum_height=self.msgs.setter('height'))
        self.scroll.add_widget(self.msgs)
        
        in_bar = BoxLayout(size_hint_y=0.1, padding=5)
        self.ti = TextInput(hint_text="Command...", background_color=(0.1, 0.1, 0.1, 1), foreground_color=(0, 0.8, 1, 1))
        btn_s = MDIconButton(icon="send", on_release=self.send)
        in_bar.add_widget(self.ti); in_bar.add_widget(btn_s)
        
        layout.add_widget(top); layout.add_widget(self.scroll); layout.add_widget(in_bar)
        self.add_widget(layout)

    def send(self, *args):
        if self.ti.text:
            self.msgs.add_widget(MDLabel(text=f"👤 {self.ti.text}", theme_text_color="Custom", text_color=(0, 0.8, 1, 1), size_hint_y=None, height=40))
            self.ti.text = ""

# ===== التطبيق الرئيسي =====
class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        sm = MDScreenManager()
        sm.add_widget(LockScreen(name="lock"))
        sm.add_widget(MainScreen(name="main"))
        return sm

if __name__ == "__main__":
    MainApp().run()
