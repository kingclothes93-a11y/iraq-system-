import json
import os
import random
from datetime import datetime

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager, SlideTransition
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock

# Constants
SETTINGS_FILE = "settings.json"
MESSAGES_FILE = "messages.json"
DEFAULT_PASS = "20057"

SYSTEM_RESPONSES = [
    "[SYSTEM]: Command acknowledged, Monarch.",
    "[SYSTEM]: Processing shadow extraction...",
    "[SYSTEM]: The shadows obey your will.",
    "[SYSTEM]: Mission logged successfully.",
    "[SYSTEM]: Arise.",
    "[SYSTEM]: All units on standby.",
    "[SYSTEM]: System status: Optimal."
]

def load_data(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r") as f: return json.load(f)
        except: pass
    return default

def save_data(path, data):
    try:
        with open(path, "w") as f: json.dump(data, f)
    except: pass

class MessageBubble(BoxLayout):
    def __init__(self, text, is_user=True, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.padding = [10, 5]
        
        # UI Styling
        color = (0, 0.4, 0.8, 0.7) if is_user else (0.1, 0.1, 0.1, 0.8)
        lbl = MDLabel(
            text=text, theme_text_color="Custom", text_color=(1,1,1,1),
            size_hint_y=None, halign=("right" if is_user else "left")
        )
        lbl.bind(texture_size=lambda w, v: setattr(w, 'height', v[1] + 10))
        
        with self.canvas.before:
            Color(*color)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
        self.bind(pos=lambda w,v: setattr(self.bg, 'pos', v), size=lambda w,v: setattr(self.bg, 'size', v))
        self.bind(minimum_height=self.setter('height'))
        self.add_widget(lbl)

class LockScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Image(source="bg_lock.jpg", allow_stretch=True, keep_ratio=False))
        
        self.pw = TextInput(
            password=True, hint_text="Enter Access Code", multiline=False,
            size_hint=(0.7, None), height=50, pos_hint={"center_x": 0.5, "center_y": 0.5},
            background_color=(0,0,0,0.7), foreground_color=(0,1,1,1)
        )
        self.pw.bind(on_text_validate=self.auth)
        
        btn = MDRaisedButton(
            text="LOGIN", pos_hint={"center_x": 0.5, "center_y": 0.4},
            on_release=self.auth, md_bg_color=(0, 0.5, 1, 1)
        )
        
        layout.add_widget(self.pw)
        layout.add_widget(btn)
        self.add_widget(layout)

    def auth(self, *args):
        if self.pw.text == DEFAULT_PASS:
            self.manager.current = "main"
        else:
            Snackbar(text="Access Denied!").open()

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history = load_data(MESSAGES_FILE, [])
        
        layout = FloatLayout()
        layout.add_widget(Image(source="bg_main.jpg", allow_stretch=True, keep_ratio=False))
        
        self.scroll = ScrollView(size_hint=(1, 0.88), pos_hint={"top": 1})
        self.chat_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=10)
        self.chat_list.bind(minimum_height=self.chat_list.setter('height'))
        self.scroll.add_widget(self.chat_list)
        
        input_area = BoxLayout(size_hint=(1, 0.08), pos_hint={"y": 0}, padding=5, spacing=5)
        self.ti = TextInput(hint_text="System Command...", multiline=False)
        self.ti.bind(on_text_validate=self.send)
        btn = MDIconButton(icon="send", on_release=self.send, theme_icon_color="Custom", icon_color=(0, 0.7, 1, 1))
        
        input_area.add_widget(self.ti)
        input_area.add_widget(btn)
        
        layout.add_widget(self.scroll)
        layout.add_widget(input_area)
        self.add_widget(layout)
        Clock.schedule_once(self.load_chat, 0.1)

    def load_chat(self, dt):
        for m in self.history:
            self.chat_list.add_widget(MessageBubble(text=m["text"], is_user=m["is_user"]))

    def send(self, *args):
        cmd = self.ti.text.strip()
        if not cmd: return
        self.chat_list.add_widget(MessageBubble(text=cmd, is_user=True))
        self.history.append({"text": cmd, "is_user": True})
        save_data(MESSAGES_FILE, self.history)
        self.ti.text = ""
        Clock.schedule_once(lambda dt: self.reply(), 0.5)

    def reply(self):
        resp = random.choice(SYSTEM_RESPONSES)
        self.chat_list.add_widget(MessageBubble(text=resp, is_user=False))
        self.history.append({"text": resp, "is_user": False})
        save_data(MESSAGES_FILE, self.history)
        self.scroll.scroll_y = 0

class ShadowApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        sm = MDScreenManager(transition=SlideTransition())
        sm.add_widget(LockScreen(name="lock"))
        sm.add_widget(MainScreen(name="main"))
        return sm

if __name__ == "__main__":
    ShadowApp().run()
