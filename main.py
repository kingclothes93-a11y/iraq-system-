import json
import os
import random
from kivy.resources import resource_add_path
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.dialog import MDDialog
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from kivy.core.text import LabelBase

# ===== مسارات الملفات =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BG_LOCK   = os.path.join(BASE_DIR, "bg_lock.jpg")
BG_MAIN   = os.path.join(BASE_DIR, "bg_main.jpg")
FONT_PATH = os.path.join(BASE_DIR, "cairo.ttf")

if platform == 'android':
    resource_add_path(BASE_DIR)

# ===== تسجيل الخط =====
try:
    LabelBase.register(name='Arabic', fn_regular=FONT_PATH)
    ARABIC_FONT = 'Arabic'
except Exception as e:
    print(f"Font Load Error: {e}")
    ARABIC_FONT = 'Roboto'

# ===== الإعدادات =====
MESSAGES_FILE    = os.path.join(BASE_DIR, "messages.json")
SETTINGS_FILE    = os.path.join(BASE_DIR, "settings.json")
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
            with open(path, "r", encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return default

def save_json(path, data):
    try:
        with open(path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
    except:
        pass

# ===== شاشة البداية =====
class SplashScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Image(source=BG_LOCK, allow_stretch=True, keep_ratio=False))
        title = MDLabel(
            text="SHADOW MONARCH",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0.8, 1, 1),
            font_style="H4",
            bold=True,
            font_name=ARABIC_FONT,
            pos_hint={"center_y": 0.55}
        )
        layout.add_widget(title)
        self.add_widget(layout)
        Clock.schedule_once(self.go_next, 3)

    def go_next(self, dt):
        self.manager.current = "lock"

# ===== شاشة القفل =====
class LockScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Image(source=BG_LOCK, allow_stretch=True, keep_ratio=False))

        self.password = TextInput(
            password=True,
            hint_text="Access Code",
            multiline=False,
            size_hint=(0.7, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            background_color=(0, 0, 0, 0.7),
            foreground_color=(0, 1, 0, 1),
            font_name=ARABIC_FONT,
            halign="center"
        )
        self.password.bind(on_text_validate=self.check_auth)

        btn = MDRaisedButton(
            text="LOGIN",
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            on_release=self.check_auth,
            md_bg_color=(0, 0.5, 1, 1)
        )

        layout.add_widget(self.password)
        layout.add_widget(btn)
        self.add_widget(layout)

    def check_auth(self, *args):
        settings = load_json(SETTINGS_FILE, {"password": DEFAULT_PASSWORD})
        if self.password.text == settings["password"]:
            self.manager.current = "main"
        else:
            MDSnackbar(MDSnackbarText(text="Access Denied")).open()
            self.password.text = ""

# ===== فقاعة الرسالة =====
class MessageBubble(BoxLayout):
    def __init__(self, text, is_user=True, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.padding = [15, 10]
        self.spacing = 5

        bubble_color = (0, 0.4, 0.9, 0.8) if is_user else (0.1, 0.1, 0.1, 0.7)
        halign = "right" if is_user else "left"

        lbl = MDLabel(
            text=text,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            font_name=ARABIC_FONT,
            halign=halign
        )
        lbl.bind(texture_size=lambda w, v: setattr(w, 'height', v[1] + 10))

        with self.canvas.before:
            Color(*bubble_color)
            self.bg = RoundedRectangle(
                pos=self.pos, size=self.size,
                radius=[15, 15, (0 if is_user else 15), (15 if is_user else 0)]
            )
        self.bind(pos=lambda w, v: setattr(self.bg, 'pos', v),
                  size=lambda w, v: setattr(self.bg, 'size', v))
        self.bind(minimum_height=self.setter('height'))
        self.add_widget(lbl)

# ===== الشاشة الرئيسية =====
class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history = load_json(MESSAGES_FILE, [])
        self.dialog = None
        self._ui()

    def _ui(self):
        layout = FloatLayout()
        layout.add_widget(Image(source=BG_MAIN, allow_stretch=True, keep_ratio=False))

        # ===== شريط العنوان =====
        top_bar = BoxLayout(
            size_hint=(1, 0.07),
            pos_hint={"top": 1},
            padding=10,
            spacing=5
        )
        with top_bar.canvas.before:
            Color(0, 0, 0, 0.85)
            self.top_bg = RoundedRectangle(pos=top_bar.pos, size=top_bar.size)
        top_bar.bind(
            pos=lambda w, v: setattr(self.top_bg, 'pos', v),
            size=lambda w, v: setattr(self.top_bg, 'size', v)
        )

        title_lbl = MDLabel(
            text="SHADOW MONARCH SYSTEM",
            halign="left",
            theme_text_color="Custom",
            text_color=(0, 0.8, 1, 1),
            bold=True,
            font_name=ARABIC_FONT
        )

        # زر مسح المحادثة
        clear_btn = MDIconButton(
            icon="delete",
            theme_text_color="Custom",
            text_color=(1, 0.2, 0.2, 1),
            on_release=self.confirm_clear
        )

        # زر تغيير الباسورد
        pass_btn = MDIconButton(
            icon="lock-reset",
            theme_text_color="Custom",
            text_color=(0, 0.8, 1, 1),
            on_release=self.change_password_dialog
        )

        top_bar.add_widget(title_lbl)
        top_bar.add_widget(pass_btn)
        top_bar.add_widget(clear_btn)

        # ===== منطقة الرسائل =====
        self.scroll = ScrollView(size_hint=(1, 0.83), pos_hint={"top": 0.93})
        self.chat_list = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=15,
            padding=15
        )
        self.chat_list.bind(minimum_height=self.chat_list.setter('height'))
        self.scroll.add_widget(self.chat_list)

        # ===== شريط الإدخال =====
        input_container = BoxLayout(
            size_hint=(1, 0.08),
            pos_hint={"y": 0},
            padding=10,
            spacing=10
        )
        with input_container.canvas.before:
            Color(0, 0, 0, 0.9)
            self.input_bg = RoundedRectangle(pos=input_container.pos, size=input_container.size)
        input_container.bind(
            pos=lambda w, v: setattr(self.input_bg, 'pos', v),
            size=lambda w, v: setattr(self.input_bg, 'size', v)
        )

        self.ti = TextInput(
            hint_text="Enter Command...",
            multiline=False,
            font_name=ARABIC_FONT,
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0, 0.5, 1, 1)
        )
        self.ti.bind(on_text_validate=self.send)

        btn = MDIconButton(
            icon="send",
            theme_text_color="Custom",
            text_color=(0, 0.5, 1, 1),
            on_release=self.send
        )

        input_container.add_widget(self.ti)
        input_container.add_widget(btn)

        layout.add_widget(top_bar)
        layout.add_widget(self.scroll)
        layout.add_widget(input_container)
        self.add_widget(layout)
        Clock.schedule_once(self.load_old, 0.5)

    def load_old(self, dt):
        for m in self.history:
            self.chat_list.add_widget(
                MessageBubble(text=m["text"], is_user=m["is_user"])
            )
        self.scroll.scroll_y = 0

    def send(self, *args):
        val = self.ti.text.strip()
        if not val:
            return
        self.chat_list.add_widget(MessageBubble(text=val, is_user=True))
        self.history.append({"text": val, "is_user": True})
        save_json(MESSAGES_FILE, self.history)
        self.ti.text = ""
        Clock.schedule_once(lambda dt: self.reply(), 1)

    def reply(self):
        res = random.choice(SYSTEM_RESPONSES)
        self.chat_list.add_widget(MessageBubble(text=res, is_user=False))
        self.history.append({"text": res, "is_user": False})
        save_json(MESSAGES_FILE, self.history)
        self.scroll.scroll_y = 0

    # ===== مسح المحادثة =====
    def confirm_clear(self, *args):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            text="هل تريد مسح كل المحادثة؟",
            buttons=[
                MDFlatButton(
                    text="إلغاء",
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="مسح",
                    md_bg_color=(1, 0.2, 0.2, 1),
                    on_release=self.clear_chat
                ),
            ]
        )
        self.dialog.open()

    def clear_chat(self, *args):
        self.dialog.dismiss()
        self.chat_list.clear_widgets()
        self.history = []
        save_json(MESSAGES_FILE, [])
        MDSnackbar(MDSnackbarText(text="تم مسح المحادثة")).open()

    # ===== تغيير الباسورد =====
    def change_password_dialog(self, *args):
        if self.dialog:
            self.dialog.dismiss()

        self.new_pass_input = TextInput(
            hint_text="الباسورد الجديد",
            password=True,
            multiline=False,
            size_hint=(1, None),
            height=45,
            font_name=ARABIC_FONT,
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1)
        )

        self.dialog = MDDialog(
            title="تغيير كلمة السر",
            type="custom",
            content_cls=self.new_pass_input,
            buttons=[
                MDFlatButton(
                    text="إلغاء",
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="حفظ",
                    md_bg_color=(0, 0.5, 1, 1),
                    on_release=self.save_new_password
                ),
            ]
        )
        self.dialog.open()

    def save_new_password(self, *args):
        new_pass = self.new_pass_input.text.strip()
        if len(new_pass) < 4:
            MDSnackbar(MDSnackbarText(text="الباسورد قصير، 4 أحرف على الأقل")).open()
            return
        save_json(SETTINGS_FILE, {"password": new_pass})
        self.dialog.dismiss()
        MDSnackbar(MDSnackbarText(text="تم تغيير كلمة السر ✓")).open()

# ===== تشغيل التطبيق =====
class ShadowApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        sm = MDScreenManager(transition=SlideTransition())
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(LockScreen(name="lock"))
        sm.add_widget(MainScreen(name="main"))
        return sm

if __name__ == "__main__":
    ShadowApp().run()
