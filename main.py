import sys
import os
import sqlite3
import datetime
import hashlib
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.animation import Animation

# Colors Configuration
C = {
    'bg': (0.02, 0.0, 0.06, 1),
    'header': (0.06, 0.0, 0.16, 1),
    'card': (0.10, 0.0, 0.22, 0.92),
    'purple': (0.55, 0.0, 1.0, 1),
    'purple2': (0.35, 0.0, 0.75, 1),
    'green': (0.0, 0.8, 0.4, 1),
    'red': (0.9, 0.1, 0.2, 1),
    'text': (0.95, 0.95, 1.0, 1),
}

DB = 'shadow.db'

def init_db():
    with sqlite3.connect(DB) as con:
        c = con.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS profile (id INTEGER PRIMARY KEY, shadow_id TEXT, level INTEGER DEFAULT 1)')
        c.execute('SELECT COUNT(*) FROM profile')
        if c.fetchone()[0] == 0:
            sid = 'SM-' + hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()[:8].upper()
            c.execute('INSERT INTO profile (shadow_id) VALUES (?)', (sid,))

def apply_bg(widget, color, radius=0):
    with widget.canvas.before:
        Color(*color)
        if radius:
            widget._bg = RoundedRectangle(pos=widget.pos, size=widget.size, radius=[dp(radius)])
        else:
            widget._bg = Rectangle(pos=widget.pos, size=widget.size)
    widget.bind(pos=lambda i,v: setattr(i._bg,'pos',v), size=lambda i,v: setattr(i._bg,'size',v))

def styled_btn(text, color=None, radius=10, **kwargs):
    color = color or C['purple2']
    btn = Button(text=text, background_color=(0,0,0,0), **kwargs)
    apply_bg(btn, color, radius)
    return btn

class SplashScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'lock'), 2)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        apply_bg(root, (0,0,0,1))
        root.add_widget(Label(text="MALEK DHALAL", font_size=dp(40), bold=True, color=C['purple']))
        self.add_widget(root)

class LockScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pin = ""
        root = FloatLayout()
        if os.path.exists('bg_lock.jpg'):
            root.add_widget(Image(source='bg_lock.jpg', allow_stretch=True, keep_ratio=False))
        else:
            apply_bg(root, C['bg'])
        
        self.display = Label(text="ENTER SECRET CODE", pos_hint={'center_y': 0.8}, font_size=dp(22), color=C['purple'], bold=True)
        root.add_widget(self.display)

        grid = GridLayout(cols=3, size_hint=(0.8, 0.45), pos_hint={'center_x': 0.5, 'center_y': 0.35}, spacing=dp(10))
        for i in range(1, 10):
            btn = styled_btn(str(i), font_size=dp(24), color=C['card'])
            btn.bind(on_press=self.press)
            grid.add_widget(btn)
        
        btn_clr = styled_btn("<", color=C['red'], font_size=dp(24))
        btn_clr.bind(on_press=self.clear)
        grid.add_widget(btn_clr)
        
        btn_0 = styled_btn("0", font_size=dp(24), color=C['card'])
        btn_0.bind(on_press=self.press)
        grid.add_widget(btn_0)

        btn_ok = styled_btn("OK", color=C['purple'], font_size=dp(18))
        btn_ok.bind(on_press=self.validate)
        grid.add_widget(btn_ok)

        root.add_widget(grid)
        self.add_widget(root)

    def press(self, instance):
        if len(self.pin) < 5:
            self.pin += instance.text
            self.display.text = "*" * len(self.pin)

    def clear(self, *a):
        self.pin = ""
        self.display.text = "ENTER SECRET CODE"

    def validate(self, *a):
        if self.pin == "20057":
            self.manager.current = 'main'
        else:
            self.clear()
            self.display.text = "WRONG CODE!"

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_open = False
        self.root = FloatLayout()
        
        # 1. Background Layer
        if os.path.exists('bg_main.jpg'):
            self.root.add_widget(Image(source='bg_main.jpg', allow_stretch=True, keep_ratio=False))
        else:
            apply_bg(self.root, C['bg'])

        # 2. Header Layer
        header = BoxLayout(size_hint=(1, 0.08), pos_hint={'top': 1}, padding=dp(10))
        apply_bg(header, C['header'])
        
        menu_trigger = Button(text="[b]≡[/b]", markup=True, font_size=dp(30), size_hint=(None, 1), width=dp(60), background_color=(0,0,0,0))
        menu_trigger.bind(on_press=self.toggle_menu)
        header.add_widget(menu_trigger)
        header.add_widget(Label(text="MALEK DHALAL", bold=True, color=C['purple']))
        self.root.add_widget(header)

        # 3. Transparent Close Layer (Above Main, Below Menu)
        self.close_layer = Button(size_hint=(1,1), background_color=(0,0,0,0), disabled=True, opacity=0)
        self.close_layer.bind(on_press=self.toggle_menu)
        self.root.add_widget(self.close_layer)

        # 4. Navigation Panel (TOP LAYER)
        self.menu_panel = FloatLayout(size_hint=(0.8, 1), pos_hint={'x': -0.8, 'y': 0})
        apply_bg(self.menu_panel, (0.05, 0.0, 0.12, 0.95))
        
        scroll = ScrollView(size_hint=(1, 0.8), pos_hint={'top': 0.85})
        box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10), padding=dp(20))
        box.bind(minimum_height=box.setter('height'))
        
        tools = [('Tasks', 'tasks'), ('Notes', 'notes'), ('Snippets', 'snippets'), ('Calculator', 'calc'), ('Pomodoro', 'pomodoro')]
        for name, screen in tools:
            btn = styled_btn(name, size_hint_y=None, height=dp(60), color=C['card'])
            btn.bind(on_press=lambda x, s=screen: self.nav(s))
            box.add_widget(btn)
        
        scroll.add_widget(box)
        self.menu_panel.add_widget(scroll)
        self.root.add_widget(self.menu_panel)

        self.add_widget(self.root)

    def toggle_menu(self, *a):
        if self.menu_open:
            anim = Animation(pos_hint={'x': -0.8}, duration=0.2, t='out_quad')
            anim.start(self.menu_panel)
            self.close_layer.disabled = True
            self.menu_open = False
        else:
            anim = Animation(pos_hint={'x': 0}, duration=0.2, t='out_quad')
            anim.start(self.menu_panel)
            self.close_layer.disabled = False
            self.menu_open = True

    def nav(self, screen_name):
        self.toggle_menu()
        self.manager.current = screen_name

class ShadowMonarchApp(App):
    def build(self):
        init_db()
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(LockScreen(name='lock'))
        sm.add_widget(MainScreen(name='main'))
        
        for s in ['tasks', 'notes', 'snippets', 'calc', 'pomodoro']:
            sc = Screen(name=s)
            apply_bg(sc, C['bg'])
            sc.add_widget(Label(text=f"{s.upper()} SCREEN"))
            btn_back = Button(text="BACK", size_hint=(None, None), size=(dp(100), dp(50)), pos_hint={'center_x': 0.5, 'y': 0.1})
            btn_back.bind(on_press=lambda x: setattr(sm, 'current', 'main'))
            sc.add_widget(btn_back)
            sm.add_widget(sc)
        return sm

if __name__ == '__main__':
    ShadowMonarchApp().run()
