import os
import random
import string
import sqlite3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.core.text import LabelBase
from kivy.animation import Animation

# ── دعم اللغة العربية ──
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    def ar(text): return get_display(arabic_reshaper.reshape(text))
except:
    def ar(text): return text

# ── الثيم والألوان ──
C_BG = (0.02, 0.0, 0.06, 1)
C_PURPLE = (0.55, 0.0, 1.0, 1)
C_DARK = (0.1, 0, 0.2, 1)

try:
    LabelBase.register(name='Shadow', fn_regular='font.ttf')
    MY_FONT = 'Shadow'
except:
    MY_FONT = 'Roboto'

# ── قاعدة البيانات ──
conn = sqlite3.connect('shadow_system.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, content TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS stats (xp INTEGER)')
if not c.execute('SELECT * FROM stats').fetchone():
    c.execute('INSERT INTO stats VALUES (0)')
conn.commit()

# ── مكونات مخصصة ──
class ShadowBtn(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0,0,0,0)
        self.font_name = MY_FONT
        with self.canvas.before:
            Color(*C_PURPLE)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
        self.bind(pos=self._upd, size=self._upd)
    def _upd(self, *args): self.rect.pos, self.rect.size = self.pos, self.size

# ════════════════ الأدوات ════════════════

class CalcScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        self.display = TextInput(text='', readonly=True, font_size='32sp', size_hint_y=0.2, background_color=(0,0,0,0.3), foreground_color=(1,1,1,1))
        layout.add_widget(self.display)
        grid = GridLayout(cols=4, spacing=dp(5))
        for b in ['7','8','9','/', '4','5','6','*', '1','2','3','-', 'C','0','=','+']:
            btn = ShadowBtn(text=b)
            btn.bind(on_release=self.run_calc)
            grid.add_widget(btn)
        layout.add_widget(grid)
        self.add_widget(layout)
    def run_calc(self, instance):
        if instance.text == '=':
            try: self.display.text = str(eval(self.display.text))
            except: self.display.text = "Error"
        elif instance.text == 'C': self.display.text = ''
        else: self.display.text += instance.text

class PassGenScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(50), spacing=dp(20))
        self.res = Label(text="Click to Gen", font_size='22sp', font_name=MY_FONT)
        btn = ShadowBtn(text=ar("توليد كلمة سر"), size_hint_y=0.2)
        btn.bind(on_release=self.gen)
        layout.add_widget(self.res)
        layout.add_widget(btn)
        self.add_widget(layout)
    def gen(self, *args):
        p = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
        self.res.text = p
        Clipboard.copy(p)

class NoteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        self.inp = TextInput(hint_text=ar("اكتب ملاحظة..."), font_name=MY_FONT)
        btn = ShadowBtn(text=ar("حفظ الملاحظة"), size_hint_y=0.2)
        btn.bind(on_release=self.save)
        layout.add_widget(self.inp)
        layout.add_widget(btn)
        self.add_widget(layout)
    def save(self, *args):
        if self.inp.text:
            c.execute('INSERT INTO notes (content) VALUES (?)', (self.inp.text,))
            conn.commit()
            self.inp.text = ""

# ════════════════ الحاوية والنظام ════════════════

class ShadowSystem(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = ScreenManager(transition=FadeTransition())
        self.sm.add_widget(CalcScreen(name='calc'))
        self.sm.add_widget(PassGenScreen(name='passgen'))
        self.sm.add_widget(NoteScreen(name='notes'))
        self.add_widget(self.sm)

        # القائمة
        self.menu = BoxLayout(orientation='vertical', size_hint=(0.6, 1), pos_hint={'x': -0.6}, padding=dp(15), spacing=dp(10))
        with self.menu.canvas.before:
            Color(*C_DARK)
            self.m_rect = Rectangle(pos=self.menu.pos, size=self.menu.size)
        self.menu.bind(pos=self._upd_m, size=self._upd_m)
        
        for n, sn in [("Calculator", 'calc'), ("PassGen", 'passgen'), ("Notes", 'notes')]:
            b = ShadowBtn(text=n, size_hint_y=None, height=dp(50))
            b.bind(on_release=lambda x, s=sn: self.sw(s))
            self.menu.add_widget(b)
        self.add_widget(self.menu)

        self.btn = Button(text="≡", size_hint=(None,None), size=(dp(60),dp(60)), pos_hint={'top':1, 'right':1}, background_color=(0,0,0,0), font_size='35sp', color=C_PURPLE)
        self.btn.bind(on_release=self.tog)
        self.add_widget(self.btn)
        self.open = False

    def _upd_m(self, *args): self.m_rect.pos, self.m_rect.size = self.menu.pos, self.menu.size
    def tog(self, *args):
        tx = 0 if not self.open else -0.6
        Animation(pos_hint={'x': tx}, duration=0.2).start(self.menu)
        self.open = not self.open
    def sw(self, sn):
        self.sm.current = sn
        self.tog()

class ShadowApp(App):
    def build(self):
        Window.clearcolor = C_BG
        return ShadowSystem()

if __name__ == '__main__':
    ShadowApp().run()
