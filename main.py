import json
import os
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.clock import Clock

MESSAGES_FILE = "messages.json"
USER_NAME = "Shadow Monarch"

SYSTEM_RESPONSES = [
    "[SYSTEM]: Command acknowledged, Shadow Monarch.",
    "[SYSTEM]: Processing your order...",
    "[SYSTEM]: The shadows obey.",
    "[SYSTEM]: Understood. Executing now.",
    "[SYSTEM]: Your will is absolute.",
    "[SYSTEM]: Mission logged.",
    "[SYSTEM]: Standing by for your next command.",
]

import random


def load_messages():
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_messages(messages):
    try:
        with open(MESSAGES_FILE, "w") as f:
            json.dump(messages, f)
    except Exception:
        pass


# ===== شاشة كلمة السر =====
class LockScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        bg = Image(
            source="bg_lock.jpg",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0}
        )

        # طبقة داكنة
        overlay = Widget(size_hint=(1, 1), pos_hint={"x": 0, "y": 0})
        with overlay.canvas:
            Color(0, 0, 0, 0.5)
            self.ov = Rectangle(pos=overlay.pos, size=overlay.size)
        overlay.bind(
            size=lambda w, v: setattr(self.ov, 'size', v),
            pos=lambda w, v: setattr(self.ov, 'pos', v)
        )

        title = MDLabel(
            text="SHADOW MONARCH",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0.8, 1, 1),
            font_style="H5",
            bold=True,
            pos_hint={"center_x": 0.5, "center_y": 0.82}
        )

        subtitle = MDLabel(
            text="[SYSTEM]: Enter Access Code",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.6, 0.6, 0.6, 1),
            font_style="Caption",
            pos_hint={"center_x": 0.5, "center_y": 0.73}
        )

        self.password = TextInput(
            password=True,
            hint_text="● ● ● ● ●",
            multiline=False,
            size_hint=(0.75, None),
            height=52,
            pos_hint={"center_x": 0.5, "center_y": 0.56},
            background_color=(0.05, 0.05, 0.1, 0.95),
            foreground_color=(0, 1, 0, 1),
            cursor_color=(0, 1, 0, 1),
            hint_text_color=(0.35, 0.35, 0.35, 1),
            halign="center",
            font_size=22,
            padding=[15, 13]
        )
        self.password.bind(on_text_validate=self.check)

        self.error_lbl = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 0.2, 0.2, 1),
            font_style="Caption",
            pos_hint={"center_x": 0.5, "center_y": 0.47}
        )

        btn = MDRaisedButton(
            text="[ LOGIN ]",
            pos_hint={"center_x": 0.5, "center_y": 0.38},
            md_bg_color=(0, 0.5, 0.8, 1),
            on_release=self.check
        )

        layout.add_widget(bg)
        layout.add_widget(overlay)
        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(self.password)
        layout.add_widget(self.error_lbl)
        layout.add_widget(btn)
        self.add_widget(layout)

    def check(self, *args):
        if self.password.text == "20057":
            self.manager.current = "main"
        else:
            self.error_lbl.text = "[ACCESS DENIED] - Wrong Code"
            self.password.text = ""
            Clock.schedule_once(
                lambda dt: setattr(self.error_lbl, 'text', ""), 2
            )


# ===== فقاعة رسالة =====
class MessageBubble(BoxLayout):
    def __init__(self, text, is_user=True, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.padding = [10, 4]

        color = (0, 0.1, 0.2, 0.85) if is_user else (0.05, 0.05, 0.05, 0.85)
        text_color = (0, 0.9, 1, 1) if is_user else (0.7, 0.7, 0.7, 1)
        align = "right" if is_user else "left"

        lbl = MDLabel(
            text=text,
            theme_text_color="Custom",
            text_color=text_color,
            size_hint_y=None,
            halign=align,
            font_size=14
        )
        lbl.bind(texture_size=lambda w, v: setattr(w, 'height', v[1] + 10))
        lbl.bind(width=lambda w, v: setattr(w, 'text_size', (v, None)))

        with self.canvas.before:
            Color(*color)
            self.bg = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[10]
            )
        self.bind(
            pos=lambda w, v: setattr(self.bg, 'pos', v),
            size=lambda w, v: setattr(self.bg, 'size', v)
        )
        self.bind(minimum_height=self.setter('height'))
        self.add_widget(lbl)


# ===== الشاشة الرئيسية =====
class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message_history = load_messages()
        self._build_ui()

    def _build_ui(self):
        root = FloatLayout()

        bg = Image(
            source="bg_main.jpg",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0}
        )

        overlay = Widget(size_hint=(1, 1), pos_hint={"x": 0, "y": 0})
        with overlay.canvas:
            Color(0, 0, 0, 0.5)
            self.ov2 = Rectangle(pos=overlay.pos, size=overlay.size)
        overlay.bind(
            size=lambda w, v: setattr(self.ov2, 'size', v),
            pos=lambda w, v: setattr(self.ov2, 'pos', v)
        )

        main_box = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0}
        )

        # Header
        header = BoxLayout(size_hint=(1, None), height=50, padding=[15, 5])
        with header.canvas.before:
            Color(0, 0, 0, 0.7)
            self.h_rect = Rectangle(pos=header.pos, size=header.size)
        header.bind(
            pos=lambda w, v: setattr(self.h_rect, 'pos', v),
            size=lambda w, v: setattr(self.h_rect, 'size', v)
        )
        header_lbl = MDLabel(
            text="SHADOW MONARCH SYSTEM",
            theme_text_color="Custom",
            text_color=(0, 0.8, 1, 1),
            font_style="Subtitle1",
            bold=True,
            halign="center"
        )
        header.add_widget(header_lbl)

        # منطقة الرسائل
        self.scroll = ScrollView(size_hint=(1, 1))
        self.msgs_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=6,
            padding=[12, 8]
        )
        self.msgs_layout.bind(
            minimum_height=self.msgs_layout.setter('height')
        )
        self.scroll.add_widget(self.msgs_layout)

        # شريط الإدخال
        input_bar = BoxLayout(
            size_hint=(1, None),
            height=62,
            padding=[8, 6],
            spacing=5
        )
        with input_bar.canvas.before:
            Color(0.05, 0.05, 0.05, 0.97)
            self.bar_rect = Rectangle(pos=input_bar.pos, size=input_bar.size)
        input_bar.bind(
            pos=lambda w, v: setattr(self.bar_rect, 'pos', v),
            size=lambda w, v: setattr(self.bar_rect, 'size', v)
        )

        btn_plus = MDIconButton(
            icon="plus",
            theme_icon_color="Custom",
            icon_color=(0.75, 0.75, 0.75, 1),
            on_release=self.open_menu
        )

        self.ti = TextInput(
            hint_text="Enter command...",
            background_color=(0.12, 0.12, 0.12, 1),
            foreground_color=(0, 1, 0, 1),
            cursor_color=(0, 1, 0, 1),
            hint_text_color=(0.35, 0.35, 0.35, 1),
            multiline=False,
            size_hint=(1, 1),
            font_size=15,
            padding=[12, 12]
        )
        self.ti.bind(on_text_validate=self.send_message)

        btn_send = MDIconButton(
            icon="send",
            theme_icon_color="Custom",
            icon_color=(0, 0.8, 1, 1),
            on_release=self.send_message
        )

        input_bar.add_widget(btn_plus)
        input_bar.add_widget(self.ti)
        input_bar.add_widget(btn_send)

        main_box.add_widget(header)
        main_box.add_widget(self.scroll)
        main_box.add_widget(input_bar)

        root.add_widget(bg)
        root.add_widget(overlay)
        root.add_widget(main_box)
        self.add_widget(root)

        # تحميل الرسائل المحفوظة
        Clock.schedule_once(self._load_saved_messages, 0.3)

    def _load_saved_messages(self, dt):
        for msg in self.message_history:
            self._render_message(msg["text"], msg["is_user"])

    def open_menu(self, *args):
        sheet = MDListBottomSheet()
        sheet.add_item("Camera", lambda x: self.action("Camera"), icon="camera")
        sheet.add_item("Photos", lambda x: self.action("Photos"), icon="image")
        sheet.add_item("Files", lambda x: self.action("Files"), icon="file-document")
        sheet.open()

    def action(self, name):
        try:
            from android.permissions import request_permissions, Permission
            if name == "Camera":
                request_permissions([Permission.CAMERA])
            elif name == "Photos":
                request_permissions([Permission.READ_MEDIA_IMAGES])
            elif name == "Files":
                request_permissions([Permission.READ_EXTERNAL_STORAGE])
        except Exception:
            pass
        self._render_message(f"[SYSTEM]: {name} activated.", False)

    def send_message(self, *args):
        text = self.ti.text.strip()
        if not text:
            return

        # رسالة المستخدم
        user_text = f"{USER_NAME}: {text}"
        self._render_message(user_text, True)
        self.message_history.append({"text": user_text, "is_user": True})

        self.ti.text = ""

        # رد تلقائي بعد ثانية
        response = random.choice(SYSTEM_RESPONSES)
        Clock.schedule_once(
            lambda dt: self._auto_reply(response), 1.0
        )

    def _auto_reply(self, response):
        self._render_message(response, False)
        self.message_history.append({"text": response, "is_user": False})
        save_messages(self.message_history)

    def _render_message(self, text, is_user):
        bubble = MessageBubble(text=text, is_user=is_user)
        self.msgs_layout.add_widget(bubble)
        Clock.schedule_once(
            lambda dt: setattr(self.scroll, 'scroll_y', 0), 0.1
        )


# ===== التطبيق =====
class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        sm = MDScreenManager()
        sm.add_widget(LockScreen(name="lock"))
        sm.add_widget(MainScreen(name="main"))
        return sm


if __name__ == "__main__":
    MainApp().run()
