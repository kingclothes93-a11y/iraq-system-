import sys
import os
import ssl
import json
import datetime
import random
import string
import re
import sqlite3
import traceback
import hashlib
import base64
import threading

ssl._create_default_https_context = ssl._create_unverified_context

from kivy.logger import Logger
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.utils import platform
from kivy.animation import Animation

try:
    from plyer import notification, vibrator
    PLYER_OK = True
except Exception:
    PLYER_OK = False

Logger.setLevel('DEBUG')

C = {
    'bg':      (0.02, 0.0,  0.06, 1),
    'header':  (0.06, 0.0,  0.16, 1),
    'card':    (0.10, 0.0,  0.22, 0.92),
    'card2':   (0.05, 0.0,  0.14, 0.95),
    'purple':  (0.55, 0.0,  1.0,  1),
    'purple2': (0.35, 0.0,  0.75, 1),
    'green':   (0.0,  0.8,  0.4,  1),
    'red':     (0.9,  0.1,  0.2,  1),
    'gold':    (1.0,  0.8,  0.0,  1),
    'text':    (0.95, 0.95, 1.0,  1),
    'sub':     (0.65, 0.55, 0.85, 1),
    'cyan':    (0.0,  0.8,  0.9,  1),
    'orange':  (1.0,  0.5,  0.0,  1),
}

RANK_COLORS = {
    'E': (0.5, 0.5, 0.5, 1),
    'D': (0.2, 0.6, 0.2, 1),
    'C': (0.2, 0.4, 0.9, 1),
    'B': (0.6, 0.2, 0.9, 1),
    'A': (1.0, 0.5, 0.0, 1),
    'S': (1.0, 0.8, 0.0, 1),
}

DB = 'shadow.db'

def init_db():
    con = sqlite3.connect(DB)
    c = con.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS profile (
        id INTEGER PRIMARY KEY, shadow_id TEXT,
        level INTEGER DEFAULT 1, xp INTEGER DEFAULT 0,
        rank TEXT DEFAULT 'E', streak INTEGER DEFAULT 0,
        last_login TEXT, title TEXT DEFAULT 'Shadow Beginner',
        army INTEGER DEFAULT 0, power INTEGER DEFAULT 100)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT, done INTEGER DEFAULT 0, date TEXT,
        xp_reward INTEGER DEFAULT 10, priority INTEGER DEFAULT 1)''')
    c.execute('''CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, time TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS snippets (
        id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, code TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, desc TEXT, earned INTEGER DEFAULT 0, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS boss (
        id INTEGER PRIMARY KEY, name TEXT,
        hp INTEGER DEFAULT 100, max_hp INTEGER DEFAULT 100, date TEXT)''')

    c.execute('SELECT COUNT(*) FROM profile')
    if c.fetchone()[0] == 0:
        sid = 'SM-' + hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()[:8].upper()
        c.execute('INSERT INTO profile VALUES (1,?,1,0,"E",0,?,"Shadow Beginner",0,100)',
                  (sid, str(datetime.date.today())))

    c.execute('SELECT COUNT(*) FROM achievements')
    if c.fetchone()[0] == 0:
        achs = [
            ('first_shadow', 'Complete your first task', 0, ''),
            ('army_x10',     'Complete 10 tasks',        0, ''),
            ('army_x50',     'Complete 50 tasks',        0, ''),
            ('week_warrior', 'Maintain 7 day streak',    0, ''),
            ('shadow_king',  'Reach rank S',             0, ''),
            ('code_keeper',  'Save 10 code snippets',    0, ''),
            ('night_owl',    'Login after midnight',     0, ''),
            ('boss_killer',  'Defeat the daily boss',    0, ''),
        ]
        c.executemany('INSERT INTO achievements (name,desc,earned,date) VALUES (?,?,?,?)', achs)

    c.execute('SELECT COUNT(*) FROM boss')
    if c.fetchone()[0] == 0:
        bosses = ['Shadow Beast','Dark Phantom','Void Walker','Night Terror','Abyss Lord']
        c.execute('INSERT INTO boss VALUES (1,?,100,100,?)',
                  (random.choice(bosses), str(datetime.date.today())))
    con.commit()
    con.close()

def get_profile():
    try:
        con = sqlite3.connect(DB)
        c = con.cursor()
        c.execute('SELECT * FROM profile WHERE id=1')
        row = c.fetchone()
        con.close()
        if row:
            return {'shadow_id':row[1],'level':row[2],'xp':row[3],
                    'rank':row[4],'streak':row[5],'last_login':row[6],
                    'title':row[7],'army':row[8],'power':row[9]}
    except Exception:
        pass
    return {}

def update_profile(**kwargs):
    try:
        con = sqlite3.connect(DB)
        c = con.cursor()
        for k, v in kwargs.items():
            c.execute(f'UPDATE profile SET {k}=? WHERE id=1', (v,))
        con.commit()
        con.close()
    except Exception:
        pass

def add_xp(amount):
    p = get_profile()
    xp = p.get('xp', 0) + amount
    level = p.get('level', 1)
    army = p.get('army', 0) + 1
    xp_needed = level * 100
    while xp >= xp_needed:
        xp -= xp_needed
        level += 1
        xp_needed = level * 100
    ranks = {1:'E',5:'D',10:'C',20:'B',35:'A',50:'S'}
    titles = {'E':'Shadow Beginner','D':'Shadow Walker','C':'Shadow Knight',
              'B':'Shadow Hunter','A':'Shadow Lord','S':'Shadow King'}
    rank = 'E'
    for lvl, r in sorted(ranks.items()):
        if level >= lvl:
            rank = r
    update_profile(xp=xp, level=level, rank=rank, title=titles.get(rank,'Shadow Beginner'), army=army)

def vibrate_short():
    try:
        if PLYER_OK and platform == 'android':
            vibrator.vibrate(0.05)
    except Exception:
        pass

def bg(widget, color, radius=0):
    with widget.canvas.before:
        Color(*color)
        if radius:
            widget._bg = RoundedRectangle(pos=widget.pos, size=widget.size, radius=[dp(radius)])
        else:
            widget._bg = Rectangle(pos=widget.pos, size=widget.size)
    widget.bind(pos=lambda i,v: setattr(i._bg,'pos',v),
                size=lambda i,v: setattr(i._bg,'size',v))

def styled_btn(text, color=None, fg=(1,1,1,1), radius=10, font_size=15, **kwargs):
    if color is None: color = C['purple2']
    btn = Button(text=text, font_size=dp(font_size),
                 background_color=(0,0,0,0), color=fg,
                 background_normal='', **kwargs)
    with btn.canvas.before:
        Color(*color)
        btn._bg = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[dp(radius)])
    btn.bind(pos=lambda i,v: setattr(i._bg,'pos',v),
             size=lambda i,v: setattr(i._bg,'size',v))
    return btn

def lbl(text, size=14, color=None, bold=False, halign='center', **kwargs):
    if color is None: color = C['text']
    return Label(text=text, font_size=dp(size), color=color,
                 bold=bold, halign=halign, **kwargs)

def make_screen_bg(screen):
    with screen.canvas.before:
        Color(*C['bg'])
        screen._bg = Rectangle(pos=screen.pos, size=screen.size)
    screen.bind(pos=lambda i,v: setattr(i._bg,'pos',v),
                size=lambda i,v: setattr(i._bg,'size',v))

def make_header(title, back_cb=None):
    header = BoxLayout(pos_hint={'x':0,'top':1}, size_hint=(1,0.08), padding=dp(10))
    bg(header, C['header'])
    if back_cb:
        b = styled_btn('< Back', color=(0,0,0,0), fg=C['purple'], size_hint=(None,1), width=dp(80))
        b.bind(on_press=back_cb)
        header.add_widget(b)
    header.add_widget(lbl(title, size=16, color=C['purple']))
    return header

def go_back(manager, target='main'):
    manager.transition = SlideTransition(direction='right', duration=0.25)
    manager.current = target


# ══════════════════════════════════════════════════════
#  SPLASH
# ══════════════════════════════════════════════════════
class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        bg(root, (0,0,0,1))
        if os.path.exists('bg_lock.jpg'):
            root.add_widget(Image(source='bg_lock.jpg', allow_stretch=True,
                                  keep_ratio=False, size_hint=(1,1), pos_hint={'x':0,'y':0}))
        overlay = FloatLayout(size_hint=(1,1), pos_hint={'x':0,'y':0})
        with overlay.canvas.before:
            Color(0,0,0,0.5)
            self._ov = Rectangle(pos=overlay.pos, size=overlay.size)
        overlay.bind(pos=lambda i,v: setattr(self._ov,'pos',v),
                     size=lambda i,v: setattr(self._ov,'size',v))
        overlay.add_widget(lbl('MALEK DHALAL', size=38, color=C['purple'], bold=True,
                               pos_hint={'center_x':0.5,'center_y':0.60},
                               size_hint=(1,None), height=dp(60)))
        overlay.add_widget(lbl('Shadow Monarch v3.0', size=14, color=C['sub'],
                               pos_hint={'center_x':0.5,'center_y':0.50},
                               size_hint=(1,None), height=dp(28)))
        overlay.add_widget(lbl('Awakening...', size=13, color=(0.4,0.2,0.7,1),
                               pos_hint={'center_x':0.5,'center_y':0.41},
                               size_hint=(1,None), height=dp(25)))
        root.add_widget(overlay)
        self.add_widget(root)

    def on_enter(self):
        Clock.schedule_once(lambda dt: setattr(self.manager,'current','lock'), 2.5)


# ══════════════════════════════════════════════════════
#  LOCK SCREEN
# ══════════════════════════════════════════════════════
class LockScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pin_entered = ''
        root = FloatLayout()
        if os.path.exists('bg_lock.jpg'):
            root.add_widget(Image(source='bg_lock.jpg', allow_stretch=True,
                                  keep_ratio=False, size_hint=(1,1),
                                  pos_hint={'x':0,'y':0}))
        else:
            bg(root, C['bg'])

        overlay = FloatLayout(size_hint=(1,1), pos_hint={'x':0,'y':0})
        with overlay.canvas.before:
            Color(0,0,0,0.35)
            self._ov = Rectangle(pos=overlay.pos, size=overlay.size)
        overlay.bind(pos=lambda i,v: setattr(self._ov,'pos',v),
                     size=lambda i,v: setattr(self._ov,'size',v))

        # Title
        title_box = BoxLayout(
            pos_hint={'center_x':0.5,'center_y':0.88},
            size_hint=(0.9,None), height=dp(60),
            orientation='vertical')
        bg(title_box, (0,0,0,0.3), radius=12)
        title_box.add_widget(lbl('MALEK DHALAL', size=32,
                                  color=C['purple'], bold=True))
        title_box.add_widget(lbl('Shadow Monarch System', size=12,
                                  color=C['sub']))
        overlay.add_widget(title_box)

        # PIN display box
        pin_box = BoxLayout(
            pos_hint={'center_x':0.5,'center_y':0.70},
            size_hint=(0.7,None), height=dp(55),
            orientation='horizontal',
            spacing=dp(12), padding=dp(10))
        bg(pin_box, (0,0,0,0.5), radius=14)

        self.pin_dots = []
        for _ in range(5):
            dot = lbl('○', size=26, color=C['purple'])
            self.pin_dots.append(dot)
            pin_box.add_widget(dot)
        overlay.add_widget(pin_box)

        # Numpad
        numpad = BoxLayout(
            orientation='vertical',
            pos_hint={'center_x':0.5,'center_y':0.38},
            size_hint=(0.82,0.44),
            spacing=dp(10))

        for row in [['1','2','3'],['4','5','6'],
                    ['7','8','9'],['CLR','0','OK']]:
            rl = BoxLayout(spacing=dp(10))
            for t in row:
                if t == 'OK':
                    col = (0.4, 0.0, 0.85, 1)
                elif t == 'CLR':
                    col = (0.7, 0.0, 0.1, 1)
                else:
                    col = (0.15, 0.0, 0.35, 0.9)
                b = Button(
                    text=t,
                    font_size=dp(22),
                    background_color=(0,0,0,0),
                    color=(1,1,1,1),
                    background_normal='',
                    bold=True
                )
                with b.canvas.before:
                    Color(*col)
                    b._bg = RoundedRectangle(
                        pos=b.pos, size=b.size, radius=[dp(12)])
                b.bind(pos=lambda i,v: setattr(i._bg,'pos',v),
                       size=lambda i,v: setattr(i._bg,'size',v))
                b.bind(on_press=self.on_btn)
                rl.add_widget(b)
            numpad.add_widget(rl)
        overlay.add_widget(numpad)

        self.err_lbl = lbl('', size=13, color=C['red'],
                           pos_hint={'center_x':0.5,'center_y':0.10},
                           size_hint=(1,None), height=dp(28))
        overlay.add_widget(self.err_lbl)
        root.add_widget(overlay)
        self.add_widget(root)

    def on_btn(self, btn):
        t = btn.text
        vibrate_short()
        if t == 'CLR':
            self.pin_entered = self.pin_entered[:-1]
        elif t == 'OK':
            if self.pin_entered == '20057':
                self._update_login()
                self.manager.transition = FadeTransition(duration=0.4)
                self.manager.current = 'main'
            else:
                self.err_lbl.text = 'Wrong code! Try again'
                self.pin_entered = ''
                for dot in self.pin_dots:
                    dot.text = '○'
                    dot.color = C['purple']
                Clock.schedule_once(
                    lambda dt: setattr(self.err_lbl,'text',''), 2)
            return
        else:
            if len(self.pin_entered) < 5:
                self.pin_entered += t

        for i, dot in enumerate(self.pin_dots):
            if i < len(self.pin_entered):
                dot.text = '●'
                dot.color = (1,1,1,1)
            else:
                dot.text = '○'
                dot.color = C['purple']

    def _update_login(self):
        try:
            p = get_profile()
            today = str(datetime.date.today())
            last = p.get('last_login','')
            streak = p.get('streak', 0)
            if last != today:
                yesterday = str(
                    datetime.date.today() - datetime.timedelta(days=1))
                streak = streak + 1 if last == yesterday else 1
                update_profile(last_login=today, streak=streak)
            if 0 <= datetime.datetime.now().hour < 4:
                con = sqlite3.connect(DB)
                c = con.cursor()
                c.execute(
                    "UPDATE achievements SET earned=1,date=? "
                    "WHERE name='night_owl' AND earned=0", (today,))
                con.commit()
                con.close()
        except Exception:
            pass


# ══════════════════════════════════════════════════════
#  MAIN SCREEN - صورة فارغة + زر هامبرغر
# ══════════════════════════════════════════════════════
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_open = False
        root = FloatLayout()

        # الخلفية
        if os.path.exists('bg_main.jpg'):
            root.add_widget(Image(source='bg_main.jpg', allow_stretch=True,
                                  keep_ratio=False, size_hint=(1,1), pos_hint={'x':0,'y':0}))
        else:
            bg(root, (0,0,0,1))

        # تعتيم خفيف
        overlay = FloatLayout(size_hint=(1,1), pos_hint={'x':0,'y':0})
        with overlay.canvas.before:
            Color(0,0,0,0.2)
            self._ov = Rectangle(pos=overlay.pos, size=overlay.size)
        overlay.bind(pos=lambda i,v: setattr(self._ov,'pos',v),
                     size=lambda i,v: setattr(self._ov,'size',v))

        # زر الهامبرغر
        menu_btn = styled_btn('= =\n= =', color=(0,0,0,0.5),
                              font_size=28, size_hint=(None,None),
                              width=dp(55), height=dp(55),
                              pos_hint={'x':0.03,'top':0.97})
        menu_btn.bind(on_press=self.toggle_menu)
        overlay.add_widget(menu_btn)

        # ساعة صغيرة
        self.clock_lbl = lbl('', size=12, color=(1,1,1,0.7),
                             pos_hint={'right':0.97,'top':0.97},
                             size_hint=(None,None), width=dp(80), height=dp(30))
        overlay.add_widget(self.clock_lbl)

        root.add_widget(overlay)

        # القائمة الجانبية - مخفية في البداية
        self.menu_panel = FloatLayout(size_hint=(0,1), pos_hint={'x':-0.75,'y':0})
        bg(self.menu_panel, (0.03,0.0,0.10,0.97))
        self._build_menu()
        root.add_widget(self.menu_panel)

        # طبقة اغلاق القائمة
        self.close_layer = Button(size_hint=(1,1), pos_hint={'x':0,'y':0},
                                  background_color=(0,0,0,0), background_normal='')
        self.close_layer.bind(on_press=self.close_menu)
        self.close_layer.opacity = 0
        self.close_layer.disabled = True
        root.add_widget(self.close_layer)

        self.add_widget(root)
        Clock.schedule_interval(self.update_clock, 1)

    def _build_menu(self):
        scroll = ScrollView(size_hint=(1,1), pos_hint={'x':0,'y':0})
        box = BoxLayout(orientation='vertical', size_hint_y=None,
                        padding=dp(8), spacing=dp(6))
        box.bind(minimum_height=box.setter('height'))

        # رأس القائمة
        header = BoxLayout(size_hint_y=None, height=dp(80),
                           orientation='vertical', padding=dp(8))
        bg(header, C['header'])
        p = get_profile()
        header.add_widget(lbl('MALEK DHALAL', size=15, color=C['purple'], bold=True))
        header.add_widget(lbl(f'Rank: {p.get("rank","E")} | Lv.{p.get("level",1)}',
                              size=11, color=C['gold']))
        box.add_widget(header)

        tools = [
            ('⚔  Daily Tasks',    'tasks'),
            ('📝  Notes',          'notes'),
            ('💾  Code Snippets',  'snippets'),
            ('🔢  Calculator',     'calc'),
            ('⏱  Pomodoro',       'pomodoro'),
            ('🔑  Password Gen',   'passgen'),
            ('🔍  Regex Tester',   'regex'),
            ('📋  JSON Format',    'jsonf'),
            ('🔄  Base Convert',   'baseconv'),
            ('🔐  Hash Gen',       'hashgen'),
            ('📐  Unit Convert',   'unitconv'),
            ('🔒  Text Encoder',   'b64enc'),
            ('🌍  World Clock',    'worldclk'),
            ('🏆  Achievements',   'achieve'),
            ('👥  Shadow Army',    'army'),
            ('⚡  Skills',         'skills'),
        ]

        for name, screen in tools:
            btn = styled_btn(name, color=C['card'], fg=C['text'],
                             font_size=14, size_hint_y=None, height=dp(52),
                             halign='left')
            btn.bind(on_press=lambda x, s=screen: self.go_to(s))
            box.add_widget(btn)

        scroll.add_widget(box)
        self.menu_panel.add_widget(scroll)

    def toggle_menu(self, *a):
        vibrate_short()
        if self.menu_open:
            self.close_menu()
        else:
            self.open_menu()

    def open_menu(self):
        self.menu_open = True
        self.close_layer.opacity = 1
        self.close_layer.disabled = False
        anim = Animation(size_hint_x=0.75, pos_hint={'x':0,'y':0}, duration=0.25)
        anim.start(self.menu_panel)

    def close_menu(self, *a):
        self.menu_open = False
        self.close_layer.opacity = 0
        self.close_layer.disabled = True
        anim = Animation(size_hint_x=0, pos_hint={'x':-0.75,'y':0}, duration=0.2)
        anim.start(self.menu_panel)

    def go_to(self, screen):
        self.close_menu()
        Clock.schedule_once(lambda dt: self._navigate(screen), 0.25)

    def _navigate(self, screen):
        self.manager.transition = SlideTransition(direction='left', duration=0.25)
        self.manager.current = screen

    def update_clock(self, dt):
        try:
            self.clock_lbl.text = datetime.datetime.now().strftime('%H:%M:%S')
        except Exception:
            pass

    def on_enter(self):
        pass


# ══════════════════════════════════════════════════════
#  TASKS
# ══════════════════════════════════════════════════════
class TasksScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header('Daily Tasks ⚔', back_cb=lambda x: go_back(self.manager)))
        self.scroll = ScrollView(pos_hint={'x':0,'y':0.15}, size_hint=(1,0.78))
        self.tl = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(7), padding=dp(9))
        self.tl.bind(minimum_height=self.tl.setter('height'))
        self.scroll.add_widget(self.tl)
        root.add_widget(self.scroll)
        inp = BoxLayout(pos_hint={'x':0,'y':0}, size_hint=(1,0.14), padding=dp(8), spacing=dp(8))
        self.task_inp = TextInput(hint_text='New task...',
                                  background_color=C['card2'][:3]+(1,),
                                  foreground_color=C['text'], font_size=dp(14), multiline=False)
        add_btn = styled_btn('+', color=C['purple2'], size_hint=(None,1), width=dp(52))
        add_btn.bind(on_press=self.add_task)
        inp.add_widget(self.task_inp)
        inp.add_widget(add_btn)
        root.add_widget(inp)
        self.add_widget(root)
        self.refresh()

    def refresh(self):
        self.tl.clear_widgets()
        try:
            con = sqlite3.connect(DB)
            c = con.cursor()
            c.execute('SELECT * FROM tasks ORDER BY done ASC, id DESC')
            tasks = c.fetchall()
            con.close()
            for t in tasks:
                done = t[2]
                row = BoxLayout(size_hint_y=None, height=dp(55), spacing=dp(7), padding=dp(8))
                bg(row, (0.04,0.18,0.04,0.9) if done else C['card'], radius=8)
                l = lbl(t[1], size=13, color=C['green'] if done else C['text'],
                        halign='left', text_size=(Window.width*0.52, None))
                xp_l = lbl(f'+{t[4]}XP', size=10, color=C['gold'], size_hint=(None,1), width=dp(42))
                db = styled_btn('✓' if not done else '↩',
                                color=C['green'] if not done else (0.3,0.3,0.3,1),
                                size_hint=(None,1), width=dp(40))
                db.bind(on_press=lambda x, tid=t[0], d=done: self.toggle(tid, d))
                xb = styled_btn('✕', color=C['red'][:3]+(0.8,), size_hint=(None,1), width=dp(36))
                xb.bind(on_press=lambda x, tid=t[0]: self.delete(tid))
                row.add_widget(l)
                row.add_widget(xp_l)
                row.add_widget(db)
                row.add_widget(xb)
                self.tl.add_widget(row)
        except Exception:
            pass

    def add_task(self, *a):
        text = self.task_inp.text.strip()
        if text:
            try:
                con = sqlite3.connect(DB)
                c = con.cursor()
                xp = random.randint(10, 30)
                c.execute('INSERT INTO tasks (text,done,date,xp_reward,priority) VALUES (?,0,?,?,?)',
                          (text, str(datetime.date.today()), xp, 1))
                con.commit()
                con.close()
                self.task_inp.text = ''
                self.refresh()
            except Exception:
                pass

    def toggle(self, tid, done):
        try:
            con = sqlite3.connect(DB)
            c = con.cursor()
            c.execute('UPDATE tasks SET done=? WHERE id=?', (0 if done else 1, tid))
            if not done:
                c.execute('SELECT xp_reward FROM tasks WHERE id=?', (tid,))
                row = c.fetchone()
                if row:
                    add_xp(row[0])
                    dmg = random.randint(10, 25)
                    c.execute('UPDATE boss SET hp=MAX(0,hp-?) WHERE id=1', (dmg,))
                    c.execute('SELECT hp FROM boss WHERE id=1')
                    hp_row = c.fetchone()
                    if hp_row and hp_row[0] == 0:
                        c.execute("UPDATE achievements SET earned=1,date=? WHERE name='boss_killer' AND earned=0",
                                  (str(datetime.date.today()),))
            con.commit()
            con.close()
            self.refresh()
        except Exception:
            pass

    def delete(self, tid):
        try:
            con = sqlite3.connect(DB)
            c = con.cursor()
            c.execute('DELETE FROM tasks WHERE id=?', (tid,))
            con.commit()
            con.close()
            self.refresh()
        except Exception:
            pass


# ══════════════════════════════════════════════════════
#  NOTES
# ══════════════════════════════════════════════════════
class NotesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header('Notes 📝', back_cb=lambda x: go_back(self.manager)))
        self.scroll = ScrollView(pos_hint={'x':0,'y':0.18}, size_hint=(1,0.74))
        self.nl = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8), padding=dp(10))
        self.nl.bind(minimum_height=self.nl.setter('height'))
        self.scroll.add_widget(self.nl)
        root.add_widget(self.scroll)
        inp = BoxLayout(pos_hint={'x':0,'y':0}, size_hint=(1,0.17), padding=dp(8), spacing=dp(8))
        self.note_inp = TextInput(hint_text='Write a note...',
                                  background_color=C['card2'][:3]+(1,),
                                  foreground_color=C['text'], font_size=dp(14))
        add_btn = styled_btn('+', color=C['purple2'], size_hint=(None,1), width=dp(52))
        add_btn.bind(on_press=self.add_note)
        inp.add_widget(self.note_inp)
        inp.add_widget(add_btn)
        root.add_widget(inp)
        self.add_widget(root)
        self.refresh()

    def refresh(self):
        self.nl.clear_widgets()
        try:
            con = sqlite3.connect(DB)
            c = con.cursor()
            c.execute('SELECT * FROM notes ORDER BY id DESC')
            notes = c.fetchall()
            con.close()
            for n in notes:
                row = BoxLayout(size_hint_y=None, height=dp(62), spacing=dp(8), padding=dp(6))
                bg(row, C['card'], radius=8)
                preview = n[1][:55] + ('...' if len(n[1]) > 55 else '')
                l = lbl(preview, size=13, halign='left', text_size=(Window.width*0.65, None))
                t_l = lbl(n[2][-5:] if n[2] else '', size=9, color=C['sub'], size_hint=(None,1), width=dp(38))
                xb = styled_btn('✕', color=C['red'][:3]+(0.8,), size_hint=(None,1), width=dp(38))
                xb.bind(on_press=lambda x, nid=n[0]: self.delete(nid))
                row.add_widget(l)
                row.add_widget(t_l)
                row.add_widget(xb)
                self.nl.add_widget(row)
        except Exception:
            pass

    def add_note(self, *a):
        text = self.note_inp.text.strip()
        if text:
            try:
                con = sqlite3.connect(DB)
                c = con.cursor()
                c.execute('INSERT INTO notes (text,time) VALUES (?,?)',
                          (text, datetime.datetime.now().strftime('%Y-%m-%d %H:%M')))
                con.commit()
                con.close()
                self.note_inp.text = ''
                self.refresh()
            except Exception:
                pass

    def delete(self, nid):
        try:
            con = sqlite3.connect(DB)
            c = con.cursor()
            c.execute('DELETE FROM notes WHERE id=?', (nid,))
            con.commit()
            con.close()
            self.refresh()
        except Exception:
            pass


# ══════════════════════════════════════════════════════
#  SNIPPETS
# ══════════════════════════════════════════════════════
class SnippetsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header('Code Snippets 💾', back_cb=lambda x: go_back(self.manager)))
        self.scroll = ScrollView(pos_hint={'x':0,'y':0.25}, size_hint=(1,0.68))
        self.sl = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8), padding=dp(10))
        self.sl.bind(minimum_height=self.sl.setter('height'))
        self.scroll.add_widget(self.sl)
        root.add_widget(self.scroll)
        inp = BoxLayout(orientation='vertical', pos_hint={'x':0,'y':0},
                        size_hint=(1,0.24), padding=dp(8), spacing=dp(6))
        self.t_inp = TextInput(hint_text='Title...', multiline=False,
                               background_color=C['card2'][:3]+(1,), foreground_color=C['text'],
                               font_size=dp(13), size_hint_y=None, height=dp(38))
        self.c_inp = TextInput(hint_text='Code here...',
                               background_color=(0.03,0.0,0.1,1), foreground_color=(0.4,1,0.4,1),
                               font_size=dp(12))
        sb = styled_btn('Save Snippet', color=C['purple2'], size_hint_y=None, height=dp(35))
        sb.bind(on_press=self.add_snip)
        for w in [self.t_inp, self.c_inp, sb]:
            inp.add_widget(w)
        root.add_widget(inp)
        self.add_widget(root)
        self.refresh()

    def refresh(self):
        self.sl.clear_widgets()
        try:
            con = sqlite3.connect(DB)
            c = con.cursor()
            c.execute('SELECT * FROM snippets ORDER BY id DESC')
            snips = c.fetchall()
            con.close()
            for s in snips:
                card = BoxLayout(size_hint_y=None, height=dp(70), spacing=dp(8), padding=dp(8))
                bg(card, C['card2'], radius=8)
                info = BoxLayout(orientation='vertical')
                info.add_widget(lbl(s[1], size=13, bold=True, color=C['purple'], halign='left'))
                preview = s[2][:40]+'...' if len(s[2])>40 else s[2]
                info.add_widget(lbl(preview, size=11, color=(0.4,1,0.4,1), halign='left'))
                cb = styled_btn('Copy', color=(0,0.35,0.15,1), size_hint=(None,1), width=dp(55))
                cb.bind(on_press=lambda x, code=s[2]: Clipboard.copy(code))
                xb = styled_btn('✕', color=C['red'][:3]+(0.8,), size_hint=(None,1), width=dp(36))
                xb.bind(on_press=lambda x, sid=s[0]: self.delete(sid))
                card.add_widget(info)
                card.add_widget(cb)
                card.add_widget(xb)
                self.sl.add_widget(card)
        except Exception:
            pass

    def add_snip(self, *a):
        t = self.t_inp.text.strip()
        c_text = self.c_inp.text.strip()
        if t and c_text:
            try:
                con = sqlite3.connect(DB)
                cur = con.cursor()
                cur.execute('INSERT INTO snippets (title,code) VALUES (?,?)', (t, c_text))
                con.commit()
                cur.execute('SELECT COUNT(*) FROM snippets')
                if cur.fetchone()[0] >= 10:
                    cur.execute("UPDATE achievements SET earned=1,date=? WHERE name='code_keeper' AND earned=0",
                                (str(datetime.date.today()),))
                    con.commit()
                con.close()
                self.t_inp.text = ''
                self.c_inp.text = ''
                self.refresh()
            except Exception:
                pass

    def delete(self, sid):
        try:
            con = sqlite3.connect(DB)
            c = con.cursor()
            c.execute('DELETE FROM snippets WHERE id=?', (sid,))
            con.commit()
            con.close()
            self.refresh()
        except Exception:
            pass


# ══════════════════════════════════════════════════════
#  CALCULATOR
# ══════════════════════════════════════════════════════
class CalcScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.expr = ''
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header('Calculator 🔢', back_cb=lambda x: go_back(self.manager)))
        self.disp = lbl('0', size=34, color=C['text'], bold=True,
                        pos_hint={'center_x':0.5,'center_y':0.80},
                        size_hint=(0.92,None), height=dp(55), halign='right')
        self.sub_disp = lbl('', size=12, color=C['sub'],
                            pos_hint={'center_x':0.5,'center_y':0.71},
                            size_hint=(0.92,None), height=dp(22), halign='right')
        root.add_widget(self.disp)
        root.add_widget(self.sub_disp)
        grid = GridLayout(cols=4, pos_hint={'center_x':0.5,'center_y':0.37},
                          size_hint=(0.95,0.54), spacing=dp(6))
        btns = [
            ('C',(0.4,0.0,0.1,1)),('()',(0.2,0.0,0.4,1)),('%',(0.2,0.0,0.4,1)),('/',(0.35,0.0,0.7,1)),
            ('7',None),('8',None),('9',None),('×',(0.35,0.0,0.7,1)),
            ('4',None),('5',None),('6',None),('-',(0.35,0.0,0.7,1)),
            ('1',None),('2',None),('3',None),('+',(0.35,0.0,0.7,1)),
            ('HEX',(0,0.2,0.4,1)),('0',None),('.',None),('=',(0.5,0.0,0.9,1)),
        ]
        for t, col in btns:
            b = styled_btn(t, color=col if col else C['card'], font_size=18)
            b.bind(on_press=self.on_calc)
            grid.add_widget(b)
        root.add_widget(grid)
        self.add_widget(root)

    def on_calc(self, btn):
        t = btn.text
        if t == 'C':
            self.expr = ''
            self.disp.text = '0'
            self.sub_disp.text = ''
        elif t == '=':
            try:
                r = eval(self.expr.replace('×','*'))
                self.sub_disp.text = self.expr
                self.disp.text = str(r)
                self.expr = str(r)
            except Exception:
                self.disp.text = 'Error'
                self.expr = ''
        elif t == 'HEX':
            try:
                v = int(eval(self.expr.replace('×','*')))
                self.sub_disp.text = f'HEX:{hex(v)[2:].upper()} BIN:{bin(v)[2:]} OCT:{oct(v)[2:]}'
            except Exception:
                self.sub_disp.text = 'Not an integer'
        elif t == '()':
            self.expr += '('
            self.disp.text = self.expr
        else:
            self.expr += t
            self.disp.text = self.expr


# ══════════════════════════════════════════════════════
#  POMODORO
# ══════════════════════════════════════════════════════
class PomodoroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.seconds_left = 25*60
        self.running = False
        self.is_break = False
        self.sessions = 0
        self._clock = None
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header('Pomodoro Timer ⏱', back_cb=lambda x: go_back(self.manager)))
        self.mode_lbl = lbl('FOCUS', size=20, color=C['red'], bold=True,
                            pos_hint={'center_x':0.5,'center_y':0.80},
                            size_hint=(1,None), height=dp(32))
        self.timer_lbl = lbl('25:00', size=66, color=C['text'], bold=True,
                             pos_hint={'center_x':0.5,'center_y':0.65},
                             size_hint=(1,None), height=dp(85))
        self.sess_lbl = lbl('Sessions: 0', size=14, color=C['sub'],
                            pos_hint={'center_x':0.5,'center_y':0.54},
                            size_hint=(1,None), height=dp(28))
        btns = BoxLayout(pos_hint={'center_x':0.5,'center_y':0.43},
                         size_hint=(0.8,None), height=dp(55), spacing=dp(12))
        self.start_btn = styled_btn('START', color=C['green'][:3]+(1,), font_size=19)
        self.start_btn.bind(on_press=self.toggle)
        reset_btn = styled_btn('RESET', color=C['red'][:3]+(0.8,), font_size=19)
        reset_btn.bind(on_press=self.reset)
        btns.add_widget(self.start_btn)
        btns.add_widget(reset_btn)
        for w in [self.mode_lbl, self.timer_lbl, self.sess_lbl, btns]:
            root.add_widget(w)
        self.add_widget(root)

    def toggle(self, *a):
        if self.running:
            self.running = False
            if self._clock: self._clock.cancel()
            self.start_btn.text = 'START'
        else:
            self.running = True
            self._clock = Clock.schedule_interval(self.tick, 1)
            self.start_btn.text = 'STOP'

    def tick(self, dt):
        if self.seconds_left > 0:
            self.seconds_left -= 1
            m, s = divmod(self.seconds_left, 60)
            self.timer_lbl.text = f'{m:02d}:{s:02d}'
        else:
            if not self.is_break:
                self.sessions += 1
                self.sess_lbl.text = f'Sessions: {self.sessions}'
                add_xp(25)
                self.is_break = True
                self.seconds_left = 5*60
                self.mode_lbl.text = 'BREAK'
                self.mode_lbl.color = C['green']
            else:
                self.is_break = False
                self.seconds_left = 25*60
                self.mode_lbl.text = 'FOCUS'
                self.mode_lbl.color = C['red']

    def reset(self, *a):
        self.running = False
        if self._clock: self._clock.cancel()
        self.is_break = False
        self.seconds_left = 25*60
        self.timer_lbl.text = '25:00'
        self.mode_lbl.text = 'FOCUS'
        self.mode_lbl.color = C['red']
        self.start_btn.text = 'START'


# ══════════════════════════════════════════════════════
#  PASSWORD GENERATOR
# ══════════════════════════════════════════════════════
class PassGenScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inc_upper = True
        self.inc_digits = True
        self.inc_symbols = True
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header('Password Generator 🔑', back_cb=lambda x: go_back(self.manager)))
        self.result_lbl = lbl('Press Generate', size=15, color=(0.5,1,0.5,1),
                              pos_hint={'center_x':0.5,'center_y':0.73},
                              size_hint=(0.9,None), height=dp(48))
        self.len_lbl = lbl('Length: 16', size=14, color=C['text'],
                           pos_hint={'center_x':0.5,'center_y':0.62},
                           size_hint=(1,None), height=dp(25))
        self.slider = Slider(min=8, max=32, value=16, step=1,
                             pos_hint={'center_x':0.5,'center_y':0.54},
                             size_hint=(0.85,None), height=dp(40))
        self.slider.bind(value=lambda s,v: setattr(self.len_lbl,'text',f'Length: {int(v)}'))
        opts = BoxLayout(pos_hint={'center_x':0.5,'center_y':0.43},
                         size_hint=(0.85,None), height=dp(44), spacing=dp(8))
        self.bu = styled_btn('ABC', color=C['purple2'], font_size=14)
        self.bd = styled_btn('123', color=C['purple2'], font_size=14)
        self.bs = styled_btn('#@!', color=C['purple2'], font_size=14)
        self.bu.bind(on_press=lambda x: self.tog('u'))
        self.bd.bind(on_press=lambda x: self.tog('d'))
        self.bs.bind(on_press=lambda x: self.tog('s'))
        for b in [self.bu, self.bd, self.bs]: opts.add_widget(b)
        gen_btn = styled_btn('GENERATE', color=C['purple2'], font_size=19,
                             size_hint=(0.6,None), height=dp(54),
                             pos_hint={'center_x':0.5,'center_y':0.29})
        gen_btn.bind(on_press=self.generate)
        copy_btn = styled_btn('COPY', color=(0,0.35,0.15,1), font_size=14,
                              size_hint=(0.5,None), height=dp(40),
                              pos_hint={'center_x':0.5,'center_y':0.18})
        copy_btn.bind(on_press=lambda x: Clipboard.copy(self.result_lbl.text))
        for w in [self.result_lbl, self.len_lbl, self.slider, opts, gen_btn, copy_btn]:
            root.add_widget(w)
        self.add_widget(root)

    def tog(self, opt):
        if opt=='u': self.inc_upper=not self.inc_upper; self.bu.color=C['green'] if self.inc_upper else C['sub']
        elif opt=='d': self.inc_digits=not self.inc_digits; self.bd.color=C['green'] if self.inc_digits else C['sub']
        elif opt=='s': self.inc_symbols=not self.inc_symbols; self.bs.color=C['green'] if self.inc_symbols else C['sub']

    def generate(self, *a):
        chars = string.ascii_lowercase
        if self.inc_upper: chars += string.ascii_uppercase
        if self.inc_digits: chars += string.digits
        if self.inc_symbols: chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
        self.result_lbl.text = ''.join(random.choice(chars) for _ in range(int(self.slider.value)))


# ══════════════════════════════════════════════════════
#  REGEX
# ══════════════════════════════════════════════════════
class RegexScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header('Regex Tester 🔍', back_cb=lambda x: go_back(self.manager)))
        content = BoxLayout(orientation='vertical', pos_hint={'x':0,'y':0},
                            size_hint=(1,0.93), padding=dp(10), spacing=dp(8))
        content.add_widget(lbl('Pattern:', size=13, color=C['purple'], size_hint_y=None, height=dp(22), halign='left'))
        self.pat = TextInput(hint_text=r'\d+', multiline=False,
                             background_color=C['card2'][:3]+(1,), foreground_color=(1,1,0,1),
                             font_size=dp(14), size_hint_y=None, height=dp(42))
        content.add_widget(self.pat)
        content.add_widget(lbl('Test text:', size=13, color=C['purple'], size_hint_y=None, height=dp(22), halign='left'))
        self.test_inp = TextInput(hint_text='Enter text here...',
                                  background_color=C['card2'][:3]+(1,), foreground_color=C['text'],
                                  font_size=dp(13), size_hint_y=None, height=dp(80))
        content.add_widget(self.test_inp)
        tb = styled_btn('TEST', color=C['purple2'], font_size=17, size_hint_y=None, height=dp(46))
        tb.bind(on_press=self.test_regex)
        content.add_widget(tb)
        self.res = lbl('', size=13, color=C['green'], halign='left', text_size=(Window.width-dp(20), None))
        content.add_widget(self.res)
        root.add_widget(content)
        self.add_widget(root)

    def test_regex(self, *a):
        try:
            m = re.findall(self.pat.text, self.test_inp.text)
            if m:
                self.res.color = C['green']
                self.res.text = f'Found {len(m)} match(es):\n' + '\n'.join(str(x) for x in m[:12])
            else:
                self.res.color = C['red']
                self.res.text = 'No matches found'
        except Exception as e:
            self.res.color = C['gold']
            self.res.text = f'Error: {e}'


# ══════════════════════════════════════════════════════
#  JSON
# ══════════════════════════════════════════════════════
class JsonScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header('JSON Formatter 📋', back_cb=lambda x: go_back(self.manager)))
        content = BoxLayout(orientation='vertical', pos_hint={'x':0,'y':0},
                            size_hint=(1,0.93), padding=dp(10), spacing=dp(8))
        self.inp = TextInput(hint_text='Paste JSON here...',
                             background_color=(0.03,0.0,0.1,1), foreground_color=C['text'], font_size=dp(12))
        btns = BoxLayout(size_hint_y=None, height=dp(46), spacing=dp(8))
        for btn_txt, cb, col in [
            ('Format', self.fmt, C['purple2']),
            ('Validate', self.val, (0,0.3,0.15,1)),
            ('Copy', lambda x: Clipboard.copy(self.inp.text), (0.2,0.1,0,1)),
        ]:
            b = styled_btn(btn_txt, color=col, font_size=15)
            b.bind(on_press=cb)
            btns.add_widget(b)
        self.status = lbl('', size=13, color=C['green'], size_hint_y=None, height=dp(28))
        content.add_widget(self.inp)
        content.add_widget(btns)
        content.add_widget(self.status)
        root.add_widget(content)
        self.add_widget(root)

    def fmt(self, *a):
        try:
            self.inp.text = json.dumps(json.loads(self.inp.text), indent=2, ensure_ascii=False)
            self.status.color = C['green']
            self.status.text = 'Formatted successfully'
        except Exception as e:
            self.status.color = C['red']
            self.status.text = f'Error: {e}'

    def val(self, *a):
        try:
            json.loads(self.inp.text)
            self.status.color = C['green']
            self.status.text = 'Valid JSON'
        except Exception as e:
            self.status.color = C['red']
            self.status.text = f'Error: {e}'


# ══════════════════════════════════════════════════════
#  BASE CONVERTER
# ══════════════════════════════════════════════════════
class BaseConvScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header('Base Converter 🔄', back_cb=lambda x: go_back(self.manager)))
        content = BoxLayout(orientation='vertical', pos_hint={'x':0,'y':0},
                            size_hint=(1,0.93), padding=dp(15), spacing=dp(10))
        self.fields = {}
        for label_txt, key, color in [
            ('Decimal',  'dec', C['text']),
            ('Hex',      'hex', (1,0.8,0,1)),
            ('Binary',   'bin', (0.4,1,0.4,1)),
            ('Octal',    'oct', (0.6,0.8,1,1)),
        ]:
            content.add_widget(lbl(label_txt, size=13, color=C['purple'], size_hint_y=None, height=dp(20), halign='left'))
            inp = TextInput(multiline=False, background_color=C['card2'][:3]+(1,),
                            foreground_color=color, font_size=dp(14), size_hint_y=None, height=dp(42))
            self.fields[key] = inp
            content.add_widget(inp)
        cb = styled_btn('CONVERT', color=C['purple2'], font_size=17, size_hint_y=None, height=dp(50))
        cb.bind(on_press=self.convert)
        content.add_widget(cb)
        root.add_widget(content)
        self.add_widget(root)

    def convert(self, *a):
        try:
            f = self.fields
            if f['dec'].text:   val = int(f['dec'].text)
            elif f['hex'].text: val = int(f['hex'].text, 16)
            elif f['bin'].text: val = int(f['bin'].text, 2)
            elif f['oct'].text: val = int(f['oct'].text, 8)
            else: return
            f['dec'].text = str(val)
            f['hex'].text = hex(val)[2:].upper()
            f['bin'].text = bin(val)[2:]
            f['oct'].text = oct(val)[2:]
        except Exception:
            for fld in self.fields.values(): fld.text = 'Error'


# ══════════════════════════════════════════════════════
#  HASH GENERATOR
# ══════════════════════════════════════════════════════
class HashGenScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header('Hash Generator 🔐', back_cb=lambda x: go_back(self.manager)))
        content = BoxLayout(orientation='vertical', pos_hint={'x':0,'y':0},
                            size_hint=(1,0.93), padding=dp(12), spacing=dp(8))
        self.inp = TextInput(hint_text='Enter text...', background_color=C['card2'][:3]+(1,),
                             foreground_color=C['text'], font_size=dp(13), size_hint_y=None, height=dp(70))
        content.add_widget(self.inp)
        gen_btn = styled_btn('GENERATE HASH', color=C['purple2'], font_size=16, size_hint_y=None, height=dp(48))
        gen_btn.bind(on_press=self.generate)
        content.add_widget(gen_btn)
        scroll = ScrollView()
        self.result_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(6), padding=dp(4))
        self.result_box.bind(minimum_height=self.result_box.setter('height'))
        scroll.add_widget(self.result_box)
        content.add_widget(scroll)
        root.add_widget(content)
        self.add_widget(root)

    def generate(self, *a):
        if not self.inp.text: return
        self.result_box.clear_widgets()
        encoded = self.inp.text.encode('utf-8')
        for name, h_val in [
            ('MD5', hashlib.md5(encoded).hexdigest()),
            ('SHA-1', hashlib.sha1(encoded).hexdigest()),
            ('SHA-256', hashlib.sha256(encoded).hexdigest()),
            ('SHA-512', hashlib.sha512(encoded).hexdigest()),
        ]:
            card = BoxLayout(size_hint_y=None, height=dp(75), spacing=dp(8), padding=dp(8))
            bg(card, C['card2'], radius=8)
            info = BoxLayout(orientation='vertical')
            info.add_widget(lbl(name, size=13, bold=True, color=C['cyan'], halign='left'))
            info.add_widget(lbl(h_val[:38]+'...', size=10, color=C['text'], halign='left'))
            cb = styled_btn('Copy', color=(0,0.35,0.15,1), size_hint=(None,1), width=dp(55))
            cb.bind(on_press=lambda x, v=h_val: Clipboard.copy(v))
            card.add_widget(info)
            card.add_widget(cb)
            self.result_box.add_widget(card)


# ══════════════════════════════════════════════════════
#  UNIT CONVERTER
# ══════════════════════════════════════════════════════
class UnitConvScreen(Screen):
    CATEGORIES = ['Length','Weight','Temperature','Area','Speed']
    UNITS = {
        'Length':      {'m':1.0,'km':1000.0,'cm':0.01,'mm':0.001,'mile':1609.34,'ft':0.3048,'inch':0.0254},
        'Weight':      {'kg':1.0,'g':0.001,'mg':0.000001,'ton':1000.0,'lb':0.453592,'oz':0.0283495},
        'Temperature': {'C':'C','F':'F','K':'K'},
        'Area':        {'m2':1.0,'km2':1000000.0,'hectare':10000.0,'ft2':0.092903,'mile2':2589988.0},
        'Speed':       {'m/s':1.0,'km/h':0.277778,'mph':0.44704,'knot':0.514444},
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cur_cat = self.CATEGORIES[0]
        self.from_unit = None
        self.to_unit = None
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header('Unit Converter 📐', back_cb=lambda x: go_back(self.manager)))
        content = BoxLayout(orientation='vertical', pos_hint={'x':0,'y':0},
                            size_hint=(1,0.93), padding=dp(12), spacing=dp(7))
        cat_scroll = ScrollView(size_hint_y=None, height=dp(46))
        cat_box = BoxLayout(size_hint_x=None, spacing=dp(5), padding=(dp(4),0))
        cat_box.bind(minimum_width=cat_box.setter('width'))
        for cat in self.CATEGORIES:
            b = styled_btn(cat, color=C['card'], font_size=12, size_hint=(None,1), width=dp(110))
            b.bind(on_press=lambda x, c=cat: self.set_cat(c))
            cat_box.add_widget(b)
        cat_scroll.add_widget(cat_box)
        content.add_widget(cat_scroll)
        self.val_inp = TextInput(hint_text='0.0', multiline=False,
                                 background_color=C['card2'][:3]+(1,), foreground_color=C['text'],
                                 font_size=dp(15), size_hint_y=None, height=dp(46))
        content.add_widget(self.val_inp)
        self.from_scroll = ScrollView(size_hint_y=None, height=dp(46))
        self.from_box = BoxLayout(size_hint_x=None, spacing=dp(5), padding=(dp(4),0))
        self.from_box.bind(minimum_width=self.from_box.setter('width'))
        self.from_scroll.add_widget(self.from_box)
        content.add_widget(lbl('From:', size=12, color=C['sub'], size_hint_y=None, height=dp(18), halign='left'))
        content.add_widget(self.from_scroll)
        self.to_scroll = ScrollView(size_hint_y=None, height=dp(46))
        self.to_box = BoxLayout(size_hint_x=None, spacing=dp(5), padding=(dp(4),0))
        self.to_box.bind(minimum_width=self.to_box.setter('width'))
        self.to_scroll.add_widget(self.to_box)
        content.add_widget(lbl('To:', size=12, color=C['sub'], size_hint_y=None, height=dp(18), halign='left'))
        content.add_widget(self.to_scroll)
        conv_btn = styled_btn('CONVERT', color=C['purple2'], font_size=17, size_hint_y=None, height=dp(50))
        conv_btn.bind(on_press=self.convert)
        content.add_widget(conv_btn)
        self.result_lbl = lbl('', size=24, color=C['gold'], bold=True, size_hint_y=None, height=dp(52))
        content.add_widget(self.result_lbl)
        root.add_widget(content)
        self.add_widget(root)
        self.set_cat(self.cur_cat)

    def set_cat(self, cat):
        self.cur_cat = cat
        self.from_unit = None
        self.to_unit = None
        self._build_btns(self.from_box, 'from')
        self._build_btns(self.to_box, 'to')

    def _build_btns(self, box, which):
        box.clear_widgets()
        for u in self.UNITS.get(self.cur_cat, {}).keys():
            b = styled_btn(u, color=C['card2'], font_size=11, size_hint=(None,1), width=dp(80))
            b.bind(on_press=lambda x, uu=u, w=which: self.select_unit(uu, w))
            box.add_widget(b)

    def select_unit(self, unit, which):
        if which == 'from': self.from_unit = unit
        else: self.to_unit = unit

    def convert(self, *a):
        try:
            val = float(self.val_inp.text)
            if not self.from_unit or not self.to_unit:
                self.result_lbl.text = 'Select both units'
                return
            units = self.UNITS.get(self.cur_cat, {})
            if self.cur_cat == 'Temperature':
                f = units.get(self.from_unit)
                t = units.get(self.to_unit)
                base = val if f=='C' else (val-32)*5/9 if f=='F' else val-273.15
                r = base if t=='C' else base*9/5+32 if t=='F' else base+273.15
            else:
                r = val * units.get(self.from_unit,1) / units.get(self.to_unit,1)
            self.result_lbl.text = f'Result: {r:.6g}'
        except Exception:
            self.result_lbl.text = 'Input error'


# ══════════════════════════════════════════════════════
#  BASE64 ENCODER
# ══════════════════════════════════════════════════════
class Base64Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header('Text Encoder 🔒', back_cb=lambda x: go_back(self.manager)))
        content = BoxLayout(orientation='vertical', pos_hint={'x':0,'y':0},
                            size_hint=(1,0.93), padding=dp(12), spacing=dp(8))
        self.inp = TextInput(hint_text='Enter text...', background_color=C['card2'][:3]+(1,),
                             foreground_color=C['text'], font_size=dp(13), size_hint_y=None, height=dp(90))
        content.add_widget(self.inp)
        btns = BoxLayout(size_hint_y=None, height=dp(46), spacing=dp(6))
        for btn_txt, cb, col in [
            ('B64 Encode', self.encode_b64, C['purple2']),
            ('B64 Decode', self.decode_b64, (0,0.3,0.15,1)),
            ('URL Encode', self.url_encode, (0.2,0.1,0,1)),
            ('URL Decode', self.url_decode, (0.1,0.15,0.05,1)),
        ]:
            b = styled_btn(btn_txt, color=col, font_size=11)
            b.bind(on_press=cb)
            btns.add_widget(b)
        content.add_widget(btns)
        self.out = TextInput(hint_text='Result here...',
                             background_color=(0.03,0.0,0.1,1), foreground_color=(0.4,1,0.4,1),
                             font_size=dp(13), size_hint_y=None, height=dp(120))
        content.add_widget(self.out)
        copy_btn = styled_btn('COPY RESULT', color=(0,0.35,0.15,1), font_size=14,
                              size_hint_y=None, height=dp(44))
        copy_btn.bind(on_press=lambda x: Clipboard.copy(self.out.text))
        content.add_widget(copy_btn)
        root.add_widget(content)
        self.add_widget(root)

    def encode_b64(self, *a):
        try: self.out.text = base64.b64encode(self.inp.text.encode()).decode()
        except Exception as e: self.out.text = f'Error: {e}'

    def decode_b64(self, *a):
        try: self.out.text = base64.b64decode(self.inp.text.encode()).decode()
        except Exception as e: self.out.text = f'Error: {e}'

    def url_encode(self, *a):
        try:
            from urllib.parse import quote
            self.out.text = quote(self.inp.text, safe='')
        except Exception as e: self.out.text = f'Error: {e}'

    def url_decode(self, *a):
        try:
            from urllib.parse import unquote
            self.out.text = unquote(self.inp.text)
        except Exception as e: self.out.text = f'Error: {e}'


# ══════════════════════════════════════════════════════
#  WORLD CLOCK
# ══════════════════════════════════════════════════════
class WorldClockScreen(Screen):
    ZONES = [
        ('Baghdad / Mecca',    3),
        ('Riyadh / Dubai',     3),
        ('London GMT',         0),
        ('Paris CET',          1),
        ('Moscow MSK',         3),
        ('Dubai GST',          4),
        ('India IST',          5.5),
        ('Beijing CST',        8),
        ('Tokyo JST',          9),
        ('Sydney AEST',        10),
        ('New York EST',      -5),
        ('Los Angeles PST',   -8),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._clock_ev = None
        self.time_labels = {}
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header('World Clock 🌍', back_cb=lambda x: self._go_back()))
        scroll = ScrollView(pos_hint={'x':0,'y':0}, size_hint=(1,0.93))
        box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(6), padding=dp(10))
        box.bind(minimum_height=box.setter('height'))
        for name, _ in self.ZONES:
            row = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8), padding=dp(8))
            bg(row, C['card'], radius=8)
            name_lbl = lbl(name, size=13, color=C['purple'], halign='left', size_hint=(0.55,1))
            time_lbl = lbl('--:--:--', size=20, color=C['gold'], bold=True, halign='right', size_hint=(0.45,1))
            row.add_widget(name_lbl)
            row.add_widget(time_lbl)
            self.time_labels[name] = time_lbl
            box.add_widget(row)
        scroll.add_widget(box)
        root.add_widget(scroll)
        self.add_widget(root)

    def _go_back(self):
        if self._clock_ev: self._clock_ev.cancel()
        go_back(self.manager)

    def on_enter(self):
        self.update_times()
        self._clock_ev = Clock.schedule_interval(lambda dt: self.update_times(), 1)

    def on_leave(self):
        if self._clock_ev: self._clock_ev.cancel()

    def update_times(self):
        try:
            utc_now = datetime.datetime.utcnow()
            for name, offset in self.ZONES:
                local = utc_now + datetime.timedelta(hours=offset)
                self.time_labels[name].text = local.strftime('%H:%M:%S')
        except Exception:
            pass


# ══════════════════════════════════════════════════════
#  ACHIEVEMENTS
# ══════════════════════════════════════════════════════
class AchieveScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header('Achievements 🏆', back_cb=lambda x: go_back(self.manager)))
        self.scroll = ScrollView(pos_hint={'x':0,'y':0}, size_hint=(1,0.93))
        self.al = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8), padding=dp(10))
        self.al.bind(minimum_height=self.al.setter('height'))
        self.scroll.add_widget(self.al)
        root.add_widget(self.scroll)
        self.add_widget(root)

    def on_enter(self):
        self.al.clear_widgets()
        try:
            con = sqlite3.connect(DB)
            c = con.cursor()
            c.execute('SELECT * FROM achievements')
            achs = c.fetchall()
            con.close()
            for a in achs:
                earned = a[3]
                card = BoxLayout(size_hint_y=None, height=dp(72), spacing=dp(8), padding=dp(10))
                bg(card, (0.05,0.15,0.05,0.9) if earned else C['card'], radius=10)
                info = BoxLayout(orientation='vertical')
                pfx = '✅ ' if earned else '🔒 '
                info.add_widget(lbl(pfx+a[1].replace('_',' ').title(), size=14, bold=True,
                                    color=C['gold'] if earned else C['sub'], halign='left'))
                info.add_widget(lbl(a[2], size=11, color=C['text'], halign='left'))
                if earned and a[4]:
                    info.add_widget(lbl(f'Date: {a[4]}', size=10, color=C['green'], halign='left'))
                card.add_widget(info)
                self.al.add_widget(card)
        except Exception:
            pass


# ══════════════════════════════════════════════════════
#  ARMY
# ══════════════════════════════════════════════════════
class ArmyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header('Shadow Army 👥', back_cb=lambda x: go_back(self.manager)))
        card = BoxLayout(orientation='vertical',
                         pos_hint={'center_x':0.5,'center_y':0.62},
                         size_hint=(0.88,None), height=dp(220),
                         padding=dp(15), spacing=dp(10))
        bg(card, C['card'], radius=14)
        self.army_lbl   = lbl('Army: 0',       size=30, color=C['purple'], bold=True)
        self.rank_lbl   = lbl('Rank: E',        size=20, color=C['gold'])
        self.level_lbl  = lbl('Level: 1',       size=16, color=C['text'])
        self.streak_lbl = lbl('Streak: 0 days', size=14, color=C['green'])
        self.id_lbl     = lbl('Shadow ID: ...', size=12, color=C['sub'])
        self.xp_bar     = ProgressBar(max=100, value=0, size_hint=(1,None), height=dp(12))
        for w in [self.army_lbl, self.rank_lbl, self.level_lbl,
                  self.streak_lbl, self.id_lbl, self.xp_bar]:
            card.add_widget(w)
        root.add_widget(card)
        self.next_info = lbl('', size=13, color=C['text'],
                             pos_hint={'center_x':0.5,'center_y':0.22},
                             size_hint=(0.88,None), height=dp(40))
        root.add_widget(self.next_info)
        self.add_widget(root)

    def on_enter(self):
        try:
            p = get_profile()
            self.army_lbl.text   = f'Army: {p["army"]}'
            self.rank_lbl.text   = f'Rank: {p["rank"]}'
            self.rank_lbl.color  = RANK_COLORS.get(p['rank'], C['gold'])
            self.level_lbl.text  = f'Level: {p["level"]}'
            self.streak_lbl.text = f'Streak: {p["streak"]} days'
            self.id_lbl.text     = f'Shadow ID: {p["shadow_id"]}'
            xp_need = p['level'] * 100
            self.xp_bar.max = xp_need
            self.xp_bar.value = p['xp']
            nexts = {'E':'Reach Lv.5 → Rank D','D':'Reach Lv.10 → Rank C',
                     'C':'Reach Lv.20 → Rank B','B':'Reach Lv.35 → Rank A',
                     'A':'Reach Lv.50 → Rank S','S':'Max rank achieved! 👑'}
            self.next_info.text = nexts.get(p['rank'], '')
        except Exception:
            pass


# ══════════════════════════════════════════════════════
#  SKILLS
# ══════════════════════════════════════════════════════
class SkillsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header('Skills ⚡', back_cb=lambda x: go_back(self.manager)))
        self.scroll = ScrollView(pos_hint={'x':0,'y':0}, size_hint=(1,0.93))
        self.sl = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8), padding=dp(10))
        self.sl.bind(minimum_height=self.sl.setter('height'))
        self.scroll.add_widget(self.sl)
        root.add_widget(self.scroll)
        self.add_widget(root)

    def on_enter(self):
        self.sl.clear_widgets()
        try:
            p = get_profile()
            rank = p.get('rank','E')
            level = p.get('level',1)
            skills = [
                ('Shadow Step',   'E',  1,  'Basic movement in darkness'),
                ('Shadow Cloak',  'E',  3,  'Block all distractions'),
                ('Dark Vision',   'D',  5,  'See opportunities others miss'),
                ('Shadow Army',   'D',  8,  'Command your task army'),
                ('Void Strike',   'C',  12, 'Complete tasks instantly'),
                ('Shadow Domain', 'C',  18, 'Control your environment'),
                ('Royal Will',    'B',  25, 'Bend reality to your goals'),
                ('Arise!',        'A',  40, 'Summon peak productivity'),
                ('Shadow Monarch','S',  50, 'Absolute power activated'),
            ]
            rank_order = ['E','D','C','B','A','S']
            for name, req_rank, req_lvl, desc in skills:
                unlocked = (rank_order.index(rank) >= rank_order.index(req_rank) and level >= req_lvl)
                card = BoxLayout(size_hint_y=None, height=dp(72), spacing=dp(8), padding=dp(10))
                bg(card, (0.05,0.12,0.05,0.9) if unlocked else C['card2'], radius=10)
                info = BoxLayout(orientation='vertical')
                pfx = '⚡ ' if unlocked else '🔒 '
                info.add_widget(lbl(pfx+name, size=14, bold=True,
                                    color=C['gold'] if unlocked else C['sub'], halign='left'))
                info.add_widget(lbl(desc, size=11, color=C['text'], halign='left'))
                req = lbl(f'Rank {req_rank} | Lv.{req_lvl}', size=10,
                           color=C['green'] if unlocked else C['red'],
                           size_hint=(None,1), width=dp(100))
                card.add_widget(info)
                card.add_widget(req)
                self.sl.add_widget(card)
        except Exception:
            pass


# ══════════════════════════════════════════════════════
#  APP
# ══════════════════════════════════════════════════════
class ShadowMonarchApp(App):
    def build(self):
        try:
            Window.clearcolor = (0,0,0,1)
            init_db()
            sm = ScreenManager(transition=FadeTransition(duration=0.3))
            for s in [
                SplashScreen(name='splash'),
                LockScreen(name='lock'),
                MainScreen(name='main'),
                TasksScreen(name='tasks'),
                NotesScreen(name='notes'),
                SnippetsScreen(name='snippets'),
                CalcScreen(name='calc'),
                PomodoroScreen(name='pomodoro'),
                PassGenScreen(name='passgen'),
                RegexScreen(name='regex'),
                JsonScreen(name='jsonf'),
                BaseConvScreen(name='baseconv'),
                HashGenScreen(name='hashgen'),
                UnitConvScreen(name='unitconv'),
                Base64Screen(name='b64enc'),
                WorldClockScreen(name='worldclk'),
                AchieveScreen(name='achieve'),
                ArmyScreen(name='army'),
                SkillsScreen(name='skills'),
            ]:
                sm.add_widget(s)
            sm.current = 'splash'
            return sm
        except Exception as e:
            Logger.error('App', traceback.format_exc())
            return Label(text=f'ERROR: {str(e)}')

if __name__ == '__main__':
    try:
        ShadowMonarchApp().run()
    except Exception as e:
        Logger.critical('App', str(e))
        sys.exit(1)
