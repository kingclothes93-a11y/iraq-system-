import time
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.clock import Clock

# ===== شاشة كلمة السر =====
class LockScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # صورة الخلفية (جين وو الغامض) - رابط مباشر
        bg = AsyncImage(
            source="https://w0.peakpx.com/wallpaper/404/695/HD-wallpaper-sung-jin-woo-eye-glowing-blue-anime-solo-leveling.jpg",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0}
        )

        overlay = Widget(size_hint=(1, 1), pos_hint={"x": 0, "y": 0})
        with overlay.canvas:
            Color(0, 0, 0, 0.5)
            self.overlay_rect = Rectangle(pos=overlay.pos, size=overlay.size)
        overlay.bind(size=lambda w, v: setattr(self.overlay_rect, 'size', v),
                     pos=lambda w, v: setattr(self.overlay_rect, 'pos', v))

        title = MDLabel(
            text="SHADOW MONARCH",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0.8, 1, 1),
            font_style="H5",
            bold=True,
            pos_hint={"center_x": 0.5, "center_y": 0.82}
        )

        self.password_input = TextInput(
            hint_text="● ● ● ● ●",
            password=True,
            multiline=False,
            size_hint=(0.7, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            background_color=(0.05, 0.05, 0.1, 0.9),
            foreground_color=(0, 0.8, 1, 1),
            cursor_color=(0, 0.8, 1, 1)
        )

        btn_enter = MDRaisedButton(
            text="[ ARISES ]",
            size_hint=(0.5, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            md_bg_color=(0, 0.5, 0.8, 1),
            on_release=self.check_password
        )

        layout.add_widget(bg)
        layout.add_widget(overlay)
        layout.add_widget(title)
        layout.add_widget(self.password_input)
        layout.add_widget(btn_enter)
        self.add_widget(layout)

    def check_password(self, *args):
        if self.password_input.text == "20057":
            self.manager.current = "main"
        else:
            self.password_input.text = ""

# ===== الشاشة الرئيسية =====
class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical')

        # الأعلى مع صورة جين وو والظلال
        top = FloatLayout(size_hint=(1, 0.4))
        bg_main = AsyncImage(
            source="https://w0.peakpx.com/wallpaper/326/289/HD-wallpaper-sung-jin-woo-solo-leveling-anime-aesthetic-shadows.jpg",
            allow_stretch=True,
            keep_ratio=False
        )

        title_label = MDLabel(
            text="[SYSTEM]: Welcome, King Mustafa",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0.8, 1, 1),
            font_style="H6",
            bold=True,
            pos_hint={"center_x": 0.5, "center_y": 0.2}
        )

        top.add_widget(bg_main)
        top.add_widget(title_label)

        # منطقة الرسائل
        self.scroll = ScrollView(size_hint=(1, 0.45))
        self.messages_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5, padding=10)
        self.messages_layout.bind(minimum_height=self.messages_layout.setter('height'))
        self.scroll.add_widget(self.messages_layout)

        # شريط الإدخال
        input_bar = BoxLayout(size_hint=(1, 0.15), padding=5, spacing=5)
        self.text_input = TextInput(
            hint_text="Enter System Command...",
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(0, 0.8, 1, 1)
        )
        btn_send = MDIconButton(icon="send", icon_color=(0, 0.8, 1, 1), on_release=self.send_message)
        
        input_bar.add_widget(self.text_input)
        input_bar.add_widget(btn_send)

        main_layout.add_widget(top)
        main_layout.add_widget(self.scroll)
        main_layout.add_widget(input_bar)
        self.add_widget(main_layout)

    def send_message(self, *args):
        text = self.text_input.text.strip()
        if text:
            lbl = MDLabel(text=f"👤 {text}", theme_text_color="Custom", text_color=(0, 0.8, 1, 1), size_hint_y=None, height=40)
            self.messages_layout.add_widget(lbl)
            self.text_input.text = ""

# ===== التطبيق الرئيسي =====
class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        sm = MDScreenManager()
        sm.add_widget(LockScreen(name="lock"))
        sm.add_widget(MainScreen
