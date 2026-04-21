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

# ===== نظام تسجيل الخط (تم التعديل لضمان الأمان) =====
try:
    # نتأكد من أن ملف الخط اسمه cairo.ttf في المجلد الرئيسي
    LabelBase.register(name='Arabic', fn_regular='cairo.ttf')
    ARABIC_FONT = 'Arabic'
except Exception as e:
    print(f"Font Load Error: {e}")
    ARABIC_FONT = 'Roboto' # خط احتياطي في حال عدم وجود الملف لمنع الانهيار

# ===== الإعدادات الثابتة =====
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
            with open(path, "r", encoding='utf-8') as f:
                return json.load(f)
        except: pass
    return default

def save_json(path, data):
    try:
        with open(path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
    except: pass

# ===== شاشة البداية (Splash) =====
class SplashScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        # الخلفية
        layout.add_widget(Image(source="bg_lock.jpg", allow_stretch=True, keep_ratio=False))
        
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

# ===== شاشة القفل (Lock) =====
class LockScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Image(source="bg_lock.jpg", allow_stretch=True, keep_ratio=False))
        
        self.password = TextInput(
            password=True, hint_text="Access Code", multiline=False,
            size_hint=(0.7, None), height=50, pos_hint={"center_x": 0.5, "center_y": 0.5},
            background_color=(0,0,0,0.7), foreground_color=(0,1,0,1), font_name=ARABIC_FONT
        )
        self.password.bind(on_text_validate=self.check_auth)
        
        btn = MDRaisedButton(
            text="LOGIN", pos_hint={"center_x": 0.5, "center_y": 0.4},
            on_release=self.check_auth
        )
        
        layout.add_widget(self.password)
        layout.add_widget(btn)
        self.add_widget(layout)

    def check_auth(self, *args):
        settings = load_json(SETTINGS_FILE, {"password": DEFAULT_PASSWORD})
        if self.password.text == settings["password"]:
            self.manager.current = "main"
        else:
            Snackbar(text="Access Denied").open()

# ===== فقاعة الرسالة =====
class MessageBubble(BoxLayout):
    def __init__(self, text, is_user=True, timestamp="", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.padding = [10, 5]
        
        color = (0, 0.2, 0.4, 0.8) if is_user else (0.1, 0.1, 0.1, 0.8)
        lbl = MDLabel(
            text=text, theme_text_color="Custom", text_color=(1,1,1,1),
            size_hint_y=None, font_name=ARABIC_FONT, halign=("right" if is_user else "left")
        )
        lbl.bind(texture_size=lambda w, v: setattr(w, 'height', v[1] + 10))
        
        with self.canvas.before:
            Color(*color)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
        self.bind(pos=lambda w,v: setattr(self.bg, 'pos', v), size=lambda w,v: setattr(self.bg, 'size', v))
        self.bind(minimum_height=self.setter('height'))
        self.add_widget(lbl)

# ===== الشاشة الرئيسية (Main Chat) =====
class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history = load_json(MESSAGES_FILE, [])
        self._ui()

    def _ui(self):
        layout = FloatLayout()
        layout.add_widget(Image(source="bg_main.jpg", allow_stretch=True, keep_ratio=False))
        
        # منطقة الرسائل
        self.scroll = ScrollView(size_hint=(1, 0.85), pos_hint={"top": 1})
        self.chat_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=10)
        self.chat_list.bind(minimum_height=self.chat_list.setter('height'))
        self.scroll.add_widget(self.chat_list)
        
        # شريط الإدخال
        input_box = BoxLayout(size_hint=(1, 0.08), pos_hint={"y": 0}, padding=5, spacing=5)
        self.ti = TextInput(hint_text="Enter Command...", multiline=False, font_name=ARABIC_FONT)
        self.ti.bind(on_text_validate=self.send)
        btn = MDIconButton(icon="send", on_release=self.send)
        
        input_box.add_widget(self.ti)
        input_box.add_widget(btn)
        
        layout.add_widget(self.scroll)
        layout.add_widget(input_box)
        self.add_widget(layout)
        Clock.schedule_once(self.load_old, 0.2)

    def load_old(self, dt):
        for m in self.history:
            self.chat_list.add_widget(MessageBubble(text=m["text"], is_user=m["is_user"]))

    def send(self, *args):
        val = self.ti.text.strip()
        if not val: return
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
