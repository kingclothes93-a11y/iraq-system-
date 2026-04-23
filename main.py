import sys, traceback, os, json, datetime, random, string, re, ssl
ssl._create_default_https_context = ssl._create_unverified_context
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.animation import Animation

# مكتبات معالجة اللغة العربية
import arabic_reshaper
from bidi.algorithm import get_display

def ar(text):
    if not text: return ""
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

def styled_btn(text, bg=(0.15, 0.0, 0.35, 1), radius=10, font_size=16, **kwargs):
    btn = Button(text=ar(text), font_name="font.ttf", font_size=dp(font_size),
                 background_color=(0,0,0,0), color=(1,1,1,1), **kwargs)
    with btn.canvas.before:
        Color(*bg)
        btn._bg = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[dp(radius)])
    btn.bind(pos=lambda i,v: setattr(i._bg,'pos',v), size=lambda i,v: setattr(i._bg,'size',v))
    return btn

# --- الشاشة الرئيسية (AI Interface & Drawer) ---
class MainScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.main_layout = FloatLayout()
        with self.main_layout.canvas.before:
            Color(0.01, 0.01, 0.03, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        
        # Header
        header = BoxLayout(size_hint=(1, 0.08), pos_hint={'top': 1}, padding=dp(10))
        menu_btn = Button(text="☰", size_hint=(None, 1), width=dp(50), font_size=dp(25),
                          background_color=(0,0,0,0), color=(0.7, 0, 1, 1))
        menu_btn.bind(on_press=self.toggle_drawer)
        header.add_widget(menu_btn)
        header.add_widget(Label(text=ar("نظام الملك المتطور"), font_name="font.ttf", font_size=dp(18)))
        self.main_layout.add_widget(header)

        # AI View
        self.ai_area = Label(text=ar("مرحباً بك مالك..\nبانتظار أوامرك البرمجية من القائمة الجانبية"),
                             font_name="font.ttf", font_size=dp(20), halign="center", color=(0.5,0.5,0.7,1))
        self.main_layout.add_widget(self.ai_area)

        # Drawer
        self.drawer = BoxLayout(orientation='vertical', size_hint=(0.7, 1), pos_hint={'x': -0.7}, 
                                padding=dp(20), spacing=dp(15))
        with self.drawer.canvas.before:
            Color(0.05, 0.05, 0.1, 1)
            self.d_bg = Rectangle(pos=self.drawer.pos, size=self.drawer.size)
        
        self.drawer.add_widget(Label(text=ar("قائمة الأدوات"), font_name="font.ttf", 
                                    font_size=dp(24), color=(0.6,0,1,1), size_hint_y=None, height=dp(60)))
        
        tools = [("الملاحظات", 'notes'), ("الحاسبة", 'calc'), ("المهام", 'tasks'), 
                 ("الأكواد", 'snippets'), ("كلمات السر", 'passgen')]
        
        for name, screen in tools:
            btn = styled_btn(name, size_hint_y=None, height=dp(55))
            btn.bind(on_press=lambda x, s=screen: self.switch(s))
            self.drawer.add_widget(btn)

        self.add_widget(self.main_layout)
        self.add_widget(self.drawer)
        self.drawer_open = False

    def toggle_drawer(self, *args):
        target_x = 0 if not self.drawer_open else -0.7
        Animation(pos_hint={'x': target_x}, duration=0.25, t='out_quad').start(self.drawer)
        self.drawer_open = not self.drawer_open

    def switch(self, screen_name):
        self.toggle_drawer()
        self.manager.current = screen_name

# --- شاشات الأدوات (بناء الهياكل) ---
class ToolScreen(Screen):
    def __init__(self, title, **kw):
        super().__init__(**kw)
        l = BoxLayout(orientation='vertical', padding=dp(15))
        l.add_widget(styled_btn("العودة للرئيسية", size_hint_y=None, height=dp(50), 
                                bg=(0.4, 0, 0, 1), on_press=self.go_home))
        l.add_widget(Label(text=ar(title), font_name="font.ttf", font_size=dp(25), size_hint_y=None, height=dp(80)))
        self.content = BoxLayout(orientation='vertical')
        l.add_widget(self.content)
        self.add_widget(l)

    def go_home(self, *args):
        self.manager.current = 'main'

class MalikApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ToolScreen(title="الملاحظات", name='notes'))
        sm.add_widget(ToolScreen(title="الحاسبة", name='calc'))
        sm.add_widget(ToolScreen(title="المهام", name='tasks'))
        sm.add_widget(ToolScreen(title="مخزن الأكواد", name='snippets'))
        sm.add_widget(ToolScreen(title="مولد كلمات السر", name='passgen'))
        return sm

if __name__ == '__main__':
    MalikApp().run()
