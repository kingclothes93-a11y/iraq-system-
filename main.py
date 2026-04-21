import json
import os
import random
from datetime import datetime
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager, SlideTransition
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.core.text import LabelBase
# تسجيل الخط العربي - Shadow Monarch System
try:
    LabelBase.register(name='Arabic', fn_regular='cairo.ttf')
    ARABIC_FONT = 'Arabic'
except Exception:
    ARABIC_FONT = 'Roboto'




# ===== الإعدادات =====
MESSAGES_FILE = "messages.json"
SETTINGS_FILE = "settings.json"
USER_NAME = "Shadow Monarch"
DEFAULT_PASSWORD = "20057"

SYSTEM_RESPONSES = [
    "[SYSTEM]: Command acknowledged, Shadow Monarch.",
    "[SYSTEM]: Processing your order...",
    "[SYSTEM]: The shadows obey your will.",
    "[SYSTEM]: Understood. Executing now.",
    "[SYSTEM]: Your will is absolute.",
    "[SYSTEM]: Mission logged successfully.",
    "[SYSTEM]: Standing by for your next command.",
    "[SYSTEM]: All units on standby.",
    "[SYSTEM]: Shadow army ready.",
    "[SYSTEM]: Arise.",
]


def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return default


def save_json(path, data):
    try:
        with open(path, "w") as f:
            json.dump(data, f)
    except Exception:
        pass


# ===== شاشة البداية =====
class SplashScreen(MDScreen):
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

        overlay = Widget(size_hint=(1, 1))
        with overlay.canvas:
            Color(0, 0, 0, 0.6)
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
            font_style="H4",
            bold=True,
            font_name=ARABIC_FONT,
            pos_hint={"center_x": 0.5, "center_y": 0.55}
        )

        subtitle = MDLabel(
            text="SYSTEM INITIALIZING...",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            font_style="Caption",
            font_name=ARABIC_FONT,
            pos_hint={"center_x": 0.5, "center_y": 0.45}
        )

        layout.add_widget(bg)
        layout.add_widget(overlay)
        layout.add_widget(title)
        layout.add_widget(subtitle)
        self.add_widget(layout)

        Clock.schedule_once(self.go_to_lock, 2.5)

    def go_to_lock(self, dt):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "lock"


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

        overlay = Widget(size_hint=(1, 1))
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
            font_name=ARABIC_FONT,
            pos_hint={"center_x": 0.5, "center_y": 0.82}
        )

        subtitle = MDLabel(
            text="[SYSTEM]: Enter Access Code",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.6, 0.6, 0.6, 1),
            font_style="Caption",
            font_name=ARABIC_FONT,
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
            font_name=ARABIC_FONT,
            padding=[15, 13]
        )
        self.password.bind(on_text_validate=self.check)

        self.error_lbl = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 0.2, 0.2, 1),
            font_style="Caption",
            font_name=ARABIC_FONT,
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
        settings = load_json(SETTINGS_FILE, {"password": DEFAULT_PASSWORD})
        if self.password.text == settings.get("password", DEFAULT_PASSWORD):
            self.password.text = ""
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = "main"
        else:
            self.error_lbl.text = "[ACCESS DENIED] - Wrong Code"
            self.password.text = ""
            Clock.schedule_once(
                lambda dt: setattr(self.error_lbl, 'text', ""), 2
            )


# ===== فقاعة رسالة =====
class MessageBubble(BoxLayout):
    def __init__(self, text, is_user=True, timestamp="", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.padding = [10, 5]
        self.spacing = 2

        color = (0, 0.1, 0.25, 0.88) if is_user else (0.08, 0.08, 0.08, 0.88)
        text_color = (0, 0.9, 1, 1) if is_user else (0.75, 0.75, 0.75, 1)
        align = "right" if is_user else "left"

        lbl = MDLabel(
            text=text,
            theme_text_color="Custom",
            text_color=text_color,
            size_hint_y=None,
            halign=align,
            font_size=14,
            font_name=ARABIC_FONT
        )
        lbl.bind(texture_size=lambda w, v: setattr(w, 'height', v[1] + 8))
        lbl.bind(width=lambda w, v: setattr(w, 'text_size', (v, None)))

        time_lbl = MDLabel(
            text=timestamp,
            theme_text_color="Custom",
            text_color=(0.4, 0.4, 0.4, 1),
            size_hint_y=None,
            height=18,
            halign=align,
            font_size=10,
            font_name=ARABIC_FONT
        )

        self.msg_text = text

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
        self.add_widget(time_lbl)

        lbl.bind(on_touch_down=self.on_touch)

    def on_touch(self, widget, touch):
        if widget.collide_point(*touch.pos) and touch.is_double_tap:
            Clipboard.copy(self.msg_text)
            Snackbar(text="Message copied!").open()


# ===== شاشة الإعدادات =====
class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        bg = Image(
            source="bg_main.jpg",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )

        overlay = Widget(size_hint=(1, 1))
        with overlay.canvas:
            Color(0, 0, 0, 0.7)
            self.ov = Rectangle(pos=overlay.pos, size=overlay.size)
        overlay.bind(
            size=lambda w, v: setattr(self.ov, 'size', v),
            pos=lambda w, v: setattr(self.ov, 'pos', v)
        )

        header = BoxLayout(
            size_hint=(1, None),
            height=55,
            padding=[10, 5],
            pos_hint={"x": 0, "top": 1}
        )
        with header.canvas.before:
            Color(0, 0, 0, 0.8)
            self.h_rect = Rectangle(pos=header.pos, size=header.size)
        header.bind(
            pos=lambda w, v: setattr(self.h_rect, 'pos', v),
            size=lambda w, v: setattr(self.h_rect, 'size', v)
        )

        btn_back = MDIconButton(
            icon="arrow-left",
            theme_icon_color="Custom",
            icon_color=(0, 0.8, 1, 1),
            on_release=self.go_back
        )
        header_lbl = MDLabel(
            text="SETTINGS",
            theme_text_color="Custom",
            text_color=(0, 0.8, 1, 1),
            font_style="H6",
            bold=True,
            halign="center",
            font_name=ARABIC_FONT
        )
        header.add_widget(btn_back)
        header.add_widget(header_lbl)

        pw_lbl = MDLabel(
            text="Change Access Code:",
            theme_text_color="Custom",
            text_color=(0.7, 0.7, 0.7, 1),
            font_style="Subtitle1",
            font_name=ARABIC_FONT,
            pos_hint={"center_x": 0.5, "center_y": 0.65}
        )

        self.new_pw = TextInput(
            password=True,
            hint_text="New code...",
            multiline=False,
            size_hint=(0.7, None),
            height=48,
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(0, 1, 0, 1),
            cursor_color=(0, 1, 0, 1),
            hint_text_color=(0.4, 0.4, 0.4, 1),
            halign="center",
            font_size=18,
            font_name=ARABIC_FONT,
            padding=[12, 12]
        )

        btn_save_pw = MDRaisedButton(
            text="[ SAVE CODE ]",
            pos_hint={"center_x": 0.5, "center_y": 0.44},
            md_bg_color=(0, 0.5, 0.8, 1),
            on_release=self.save_password
        )

        btn_clear = MDRaisedButton(
            text="[ CLEAR ALL MESSAGES ]",
            pos_hint={"center_x": 0.5, "center_y": 0.30},
            md_bg_color=(0.7, 0.1, 0.1, 1),
            on_release=self.confirm_clear
        )

        self.status_lbl = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 1, 0.5, 1),
            font_style="Caption",
            font_name=ARABIC_FONT,
            pos_hint={"center_x": 0.5, "center_y": 0.22}
        )

        layout.add_widget(bg)
        layout.add_widget(overlay)
        layout.add_widget(header)
        layout.add_widget(pw_lbl)
        layout.add_widget(self.new_pw)
        layout.add_widget(btn_save_pw)
        layout.add_widget(btn_clear)
        layout.add_widget(self.status_lbl)
        self.add_widget(layout)

    def go_back(self, *args):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "main"

    def save_password(self, *args):
        new = self.new_pw.text.strip()
        if len(new) >= 4:
            settings = load_json(SETTINGS_FILE, {})
            settings["password"] = new
            save_json(SETTINGS_FILE, settings)
            self.new_pw.text = ""
            self.status_lbl.text = "Code updated successfully!"
            Clock.schedule_once(
                lambda dt: setattr(self.status_lbl, 'text', ""), 2
            )
        else:
            self.status_lbl.text = "Code must be 4+ characters!"
            Clock.schedule_once(
                lambda dt: setattr(self.status_lbl, 'text', ""), 2
            )

    def confirm_clear(self, *args):
        self.dialog = MDDialog(
            title="Clear Messages",
            text="Delete all saved messages?",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="DELETE",
                    md_bg_color=(0.7, 0.1, 0.1, 1),
                    on_release=self.clear_messages
                ),
            ]
        )
        self.dialog.open()

    def clear_messages(self, *args):
        self.dialog.dismiss()
        save_json(MESSAGES_FILE, [])
        self.status_lbl.text = "Messages cleared!"
        Clock.schedule_once(
            lambda dt: setattr(self.status_lbl, 'text', ""), 2
        )


# ===== الشاشة الرئيسية =====
class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message_history = load_json(MESSAGES_FILE, [])
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

        overlay = Widget(size_hint=(1, 1))
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

        header = BoxLayout(size_hint=(1, None), height=55, padding=[5, 5])
        with header.canvas.before:
            Color(0, 0, 0, 0.8)
            self.h_rect = Rectangle(pos=header.pos, size=header.size)
        header.bind(
            pos=lambda w, v: setattr(self.h_rect, 'pos', v),
            size=lambda w, v: setattr(self.h_rect, 'size', v)
        )

        self.counter_lbl = MDLabel(
            text=f"MSG: {len(self.message_history)}",
            theme_text_color="Custom",
            text_color=(0.4, 0.4, 0.4, 1),
            font_style="Caption",
            font_name=ARABIC_FONT,
            size_hint_x=None,
            width=70
        )

        header_title = MDLabel(
            text="SHADOW MONARCH",
            theme_text_color="Custom",
            text_color=(0, 0.8, 1, 1),
            font_style="Subtitle1",
            bold=True,
            halign="center",
            font_name=ARABIC_FONT
        )

        btn_settings = MDIconButton(
            icon="cog",
            theme_icon_color="Custom",
            icon_color=(0, 0.8, 1, 1),
            on_release=self.go_settings
        )

        btn_clear_chat = MDIconButton(
            icon="delete-sweep",
            theme_icon_color="Custom",
            icon_color=(0.8, 0.3, 0.3, 1),
            on_release=self.clear_chat
        )

        header.add_widget(self.counter_lbl)
        header.add_widget(header_title)
        header.add_widget(btn_clear_chat)
        header.add_widget(btn_settings)

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
            font_name=ARABIC_FONT,
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

        Clock.schedule_once(self._load_saved_messages, 0.3)

    def _load_saved_messages(self, dt):
        for msg in self.message_history:
            self._render_message(
                msg["text"], msg["is_user"], msg.get("time", ""), save=False
            )

    def go_settings(self, *args):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "settings"

    def clear_chat(self, *args):
        self.msgs_layout.clear_widgets()
        self.message_history = []
        save_json(MESSAGES_FILE, [])
        self.counter_lbl.text = "MSG: 0"
        Snackbar(text="Chat cleared!").open()

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
        t = datetime.now().strftime("%H:%M")
        self._render_message(f"[SYSTEM]: {name} activated.", False, t)

    def send_message(self, *args):
        text = self.ti.text.strip()
        if not text:
            return
        t = datetime.now().strftime("%H:%M")
        user_text = f"{USER_NAME}: {text}"
        self._render_message(user_text, True, t)
        self.ti.text = ""
        response = random.choice(SYSTEM_RESPONSES)
        Clock.schedule_once(lambda dt: self._auto_reply(response), 1.0)

    def _auto_reply(self, response):
        t = datetime.now().strftime("%H:%M")
        self._render_message(response, False, t)

    def _render_message(self, text, is_user, timestamp="", save=True):
        bubble = MessageBubble(text=text, is_user=is_user, timestamp=timestamp)
        self.msgs_layout.add_widget(bubble)
        if save:
            self.message_history.append({
                "text": text,
                "is_user": is_user,
                "time": timestamp
            })
            save_json(MESSAGES_FILE, self.message_history)
            self.counter_lbl.text = f"MSG: {len(self.message_history)}"
        Clock.schedule_once(
            lambda dt: setattr(self.scroll, 'scroll_y', 0), 0.1
        )


# ===== التطبيق =====
class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        sm = MDScreenManager()
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(LockScreen(name="lock"))
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(SettingsScreen(name="settings"))
        sm.current = "splash"
        return sm


if __name__ == "__main__":
    MainApp().run()
