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
from kivy.graphics import Color, Rectangle, RoundedRectangle, Ellipse
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.core.text import LabelBase
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.utils import platform

try:
    from plyer import notification, vibrator
    PLYER_OK = True
except:
    PLYER_OK = False

Logger.setLevel('DEBUG')

# ── Font ──────────────────────────────────────────────
FONT = 'font.ttf'
if os.path.exists(FONT):
    try:
        LabelBase.register(name='Shadow', fn_regular=FONT)
        DEFAULT_FONT = 'Shadow'
    except:
        DEFAULT_FONT = 'Roboto'
else:
    DEFAULT_FONT = 'Roboto'

# ── Arabic helper ─────────────────────────────────────
def ar(text):
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(text))
    except:
        return text

# ── Colors ────────────────────────────────────────────
C = {
    'bg':       (0.02, 0.0, 0.06, 1),
    'header':   (0.06, 0.0, 0.16, 1),
    'card':     (0.10, 0.0, 0.22, 0.92),
    'card2':    (0.05, 0.0, 0.14, 0.95),
    'purple':   (0.55, 0.0, 1.0,  1),
    'purple2':  (0.35, 0.0, 0.75, 1),
    'green':    (0.0,  0.8, 0.4,  1),
    'red':      (0.9,  0.1, 0.2,  1),
    'gold':     (1.0,  0.8, 0.0,  1),
    'text':     (0.95, 0.95, 1.0, 1),
    'sub':      (0.65, 0.55, 0.85, 1),
}

# ── Database ──────────────────────────────────────────
DB = 'shadow.db'

def init_db():
    con = sqlite3.connect(DB)
    c = con.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS profile (
        id INTEGER PRIMARY KEY,
        shadow_id TEXT,
        level INTEGER DEFAULT 1,
        xp INTEGER DEFAULT 0,
        rank TEXT DEFAULT 'E',
        streak INTEGER DEFAULT 0,
        last_login TEXT,
        title TEXT DEFAULT 'Shadow Beginner',
        army INTEGER DEFAULT 0,
        power INTEGER DEFAULT 100
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        done INTEGER DEFAULT 0,
        date TEXT,
        xp_reward INTEGER DEFAULT 10
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        time TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS snippets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        code TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        desc TEXT,
        earned INTEGER DEFAULT 0,
        date TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS boss (
        id INTEGER PRIMARY KEY,
        name TEXT,
        hp INTEGER DEFAULT 100,
        max_hp INTEGER DEFAULT 100,
        date TEXT
    )''')
    # Init profile
    c.execute('SELECT COUNT(*) FROM profile')
    if c.fetchone()[0] == 0:
        shadow_id = 'SM-' + hashlib.md5(
            str(datetime.datetime.now()).encode()).hexdigest()[:8].upper()
        c.execute('''INSERT INTO profile 
            (shadow_id, level, xp, rank, streak, last_login, title, army, power)
            VALUES (?,1,0,'E',0,?,?,0,100)''',
            (shadow_id, str(datetime.date.today()), 'Shadow Beginner'))
    # Init achievements
    c.execute('SELECT COUNT(*) FROM achievements')
    if c.fetchone()[0] == 0:
        achs = [
            ('First Shadow', 'Complete your first task', 0, ''),
            ('Shadow Army x10', 'Complete 10 tasks', 0, ''),
            ('Shadow Army x50', 'Complete 50 tasks', 0, ''),
            ('Week Warrior', '7 day streak', 0, ''),
            ('Shadow Master', 'Reach rank S', 0, ''),
            ('Code Keeper', 'Save 10 snippets', 0, ''),
            ('Night Owl', 'Login after midnight', 0, ''),
            ('Boss Slayer', 'Defeat a daily boss', 0, ''),
        ]
        c.executemany(
            'INSERT INTO achievements (name,desc,earned,date) VALUES (?,?,?,?)', achs)
    # Init boss
    c.execute('SELECT COUNT(*) FROM boss')
    if c.fetchone()[0] == 0:
        bosses = ['Shadow Beast', 'Dark Phantom', 'Void Walker',
                  'Night Terror', 'Abyss Lord']
        c.execute('''INSERT INTO boss (id,name,hp,max_hp,date) VALUES (1,?,100,100,?)''',
                  (random.choice(bosses), str(datetime.date.today())))
    con.commit()
    con.close()

def get_profile():
    con = sqlite3.connect(DB)
    c = con.cursor()
    c.execute('SELECT * FROM profile WHERE id=1')
    row = c.fetchone()
    con.close()
    if row:
        return {
            'shadow_id': row[1], 'level': row[2], 'xp': row[3],
            'rank': row[4], 'streak': row[5], 'last_login': row[6],
            'title': row[7], 'army': row[8], 'power': row[9]
        }
    return {}

def update_profile(**kwargs):
    con = sqlite3.connect(DB)
    c = con.cursor()
    for k, v in kwargs.items():
        c.execute(f'UPDATE profile SET {k}=? WHERE id=1', (v,))
    con.commit()
    con.close()

def add_xp(amount):
    p = get_profile()
    xp = p['xp'] + amount
    level = p['level']
    rank = p['rank']
    title = p['title']
    army = p['army'] + 1

    xp_needed = level * 100
    while xp >= xp_needed:
        xp -= xp_needed
        level += 1
        xp_needed = level * 100

    ranks = {1: 'E', 5: 'D', 10: 'C', 20: 'B', 35: 'A', 50: 'S'}
    titles = {
        'E': 'Shadow Beginner',
        'D': 'Shadow Walker',
        'C': 'Shadow Knight',
        'B': 'Shadow Hunter',
        'A': 'Shadow Lord',
        'S': 'Shadow Monarch'
    }
    for lvl, r in sorted(ranks.items()):
        if level >= lvl:
            rank = r
    title = titles.get(rank, title)
    update_profile(xp=xp, level=level, rank=rank, title=title, army=army)
    check_achievements(army=army, rank=rank)

def check_achievements(army=0, rank='E'):
    con = sqlite3.connect(DB)
    c = con.cursor()
    today = str(datetime.date.today())
    if army >= 1:
        c.execute("UPDATE achievements SET earned=1, date=? WHERE name='First Shadow' AND earned=0", (today,))
    if army >= 10:
        c.execute("UPDATE achievements SET earned=1, date=? WHERE name='Shadow Army x10' AND earned=0", (today,))
    if army >= 50:
        c.execute("UPDATE achievements SET earned=1, date=? WHERE name='Shadow Army x50' AND earned=0", (today,))
    if rank == 'S':
        c.execute("UPDATE achievements SET earned=1, date=? WHERE name='Shadow Master' AND earned=0", (today,))
    con.commit()
    con.close()

# ── Helpers ───────────────────────────────────────────
def bg(widget, color, radius=0):
    with widget.canvas.before:
        Color(*color)
        if radius:
            widget._bg = RoundedRectangle(
                pos=widget.pos, size=widget.size, radius=[dp(radius)])
        else:
            widget._bg = Rectangle(pos=widget.pos, size=widget.size)
    widget.bind(
        pos=lambda i, v: setattr(i._bg, 'pos', v),
        size=lambda i, v: setattr(i._bg, 'size', v))

def styled_btn(text, color=None, fg=(1,1,1,1), radius=10,
               font_size=15, markup=False, **kwargs):
    if color is None:
        color = C['purple2']
    btn = Button(
        text=text, markup=markup,
        font_size=dp(font_size),
        font_name=DEFAULT_FONT,
        background_color=(0,0,0,0),
        color=fg, background_normal='',
        **kwargs
    )
    with btn.canvas.before:
        Color(*color)
        btn._bg = RoundedRectangle(
            pos=btn.pos, size=btn.size, radius=[dp(radius)])
    btn.bind(
        pos=lambda i,v: setattr(i._bg,'pos',v),
        size=lambda i,v: setattr(i._bg,'size',v))
    return btn

def lbl(text, size=14, color=None, bold=False,
        halign='center', markup=False, **kwargs):
    if color is None:
        color = C['text']
    return Label(
        text=text, font_size=dp(size),
        font_name=DEFAULT_FONT,
        color=color, bold=bold,
        halign=halign, markup=markup,
        **kwargs)

def make_screen_bg(screen):
    with screen.canvas.before:
        Color(*C['bg'])
        screen._bg = Rectangle(pos=screen.pos, size=screen.size)
    screen.bind(
        pos=lambda i,v: setattr(i._bg,'pos',v),
        size=lambda i,v: setattr(i._bg,'size',v))

def make_header(title, back_cb=None):
    header = BoxLayout(
        pos_hint={'x':0,'top':1},
        size_hint=(1, 0.08), padding=dp(10))
    bg(header, C['header'])
    if back_cb:
        b = styled_btn('< Back', color=(0,0,0,0),
                       fg=C['purple'], size_hint=(None,1), width=dp(80))
        b.bind(on_press=back_cb)
        header.add_widget(b)
    header.add_widget(lbl(f'[b]{title}[/b]', size=17,
                          color=C['purple'], markup=True))
    return header

def vibrate_short():
    try:
        if PLYER_OK and platform == 'android':
            vibrator.vibrate(0.05)
    except:
        pass

def send_notification(title, msg):
    try:
        if PLYER_OK:
            notification.notify(title=title, message=msg, timeout=3)
    except:
        pass

# ── Rank colors ───────────────────────────────────────
RANK_COLORS = {
    'E': (0.5, 0.5, 0.5, 1),
    'D': (0.2, 0.6, 0.2, 1),
    'C': (0.2, 0.4, 0.9, 1),
    'B': (0.6, 0.2, 0.9, 1),
    'A': (1.0, 0.5, 0.0, 1),
    'S': (1.0, 0.8, 0.0, 1),
}

# ═══════════════════════════════════════════════════════
#  SPLASH SCREEN
# ═══════════════════════════════════════════════════════
class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        bg(layout, C['bg'])

        self.title = lbl('[b]SHADOW MONARCH[/b]', size=36,
                         color=(0.6, 0.0, 1.0, 0), markup=True,
                         pos_hint={'center_x':0.5,'center_y':0.6},
                         size_hint=(1, None), height=dp(60))
        self.sub = lbl('System v3.0', size=14,
                       color=(0.5, 0.3, 0.9, 0),
                       pos_hint={'center_x':0.5,'center_y':0.50},
                       size_hint=(1, None), height=dp(30))
        self.sub2 = lbl('Arise...', size=12,
                        color=(0.4, 0.2, 0.7, 0),
                        pos_hint={'center_x':0.5,'center_y':0.42},
                        size_hint=(1, None), height=dp(25))

        layout.add_widget(self.title)
        layout.add_widget(self.sub)
        layout.add_widget(self.sub2)
        self.add_widget(layout)

    def on_enter(self):
        self.title.color = (0.6, 0.0, 1.0, 1)
        self.sub.color   = (0.5, 0.3, 0.9, 1)
        self.sub2.color  = (0.4, 0.2, 0.7, 1)
        Clock.schedule_once(lambda dt: setattr(
            self.manager, 'current', 'lock'), 2.5)

# ═══════════════════════════════════════════════════════
#  LOCK SCREEN
# ═══════════════════════════════════════════════════════
class LockScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        try:
            if os.path.exists('bg_lock.jpg'):
                layout.add_widget(Image(
                    source='bg_lock.jpg', allow_stretch=True,
                    keep_ratio=False, size_hint=(1,1),
                    pos_hint={'x':0,'y':0}))
            else:
                bg(layout, C['bg'])
        except:
            bg(layout, C['bg'])

        overlay = FloatLayout(size_hint=(1,1), pos_hint={'x':0,'y':0})
        with overlay.canvas.before:
            Color(0, 0, 0, 0.5)
            overlay._ov = Rectangle(pos=overlay.pos, size=overlay.size)
        overlay.bind(
            pos=lambda i,v: setattr(i._ov,'pos',v),
            size=lambda i,v: setattr(i._ov,'size',v))

        overlay.add_widget(lbl('[b]SHADOW MONARCH[/b]', size=32,
            color=C['purple'], markup=True,
            pos_hint={'center_x':0.5,'center_y':0.84},
            size_hint=(1,None), height=dp(55)))
        overlay.add_widget(lbl('Enter PIN to Access System', size=13,
            color=C['sub'],
            pos_hint={'center_x':0.5,'center_y':0.75},
            size_hint=(1,None), height=dp(25)))

        self.pin_display = lbl('o  o  o  o  o', size=26,
            color=C['purple'],
            pos_hint={'center_x':0.5,'center_y':0.62},
            size_hint=(1,None), height=dp(40))
        self.pin_entered = ''
        overlay.add_widget(self.pin_display)

        numpad = BoxLayout(orientation='vertical',
            pos_hint={'center_x':0.5,'center_y':0.36},
            size_hint=(0.72, 0.42), spacing=dp(8))
        for row in [['1','2','3'],['4','5','6'],
                    ['7','8','9'],['<','0','OK']]:
            rl = BoxLayout(orientation='horizontal', spacing=dp(8))
            for t in row:
                b = styled_btn(t,
                    color=C['purple2'] if t=='OK' else C['card'],
                    font_size=18)
                b.bind(on_press=self.on_btn)
                rl.add_widget(b)
            numpad.add_widget(rl)
        overlay.add_widget(numpad)

        self.err = lbl('', size=13, color=C['red'],
            pos_hint={'center_x':0.5,'center_y':0.10},
            size_hint=(1,None), height=dp(30))
        overlay.add_widget(self.err)

        layout.add_widget(overlay)
        self.add_widget(layout)

    def on_btn(self, btn):
        t = btn.text
        vibrate_short()
        if t == '<':
            self.pin_entered = self.pin_entered[:-1]
        elif t == 'OK':
            if self.pin_entered == '20057':
                self.update_login()
                self.manager.transition = FadeTransition(duration=0.4)
                self.manager.current = 'main'
            else:
                self.err.text = 'Access Denied!'
                self.pin_entered = ''
                self.pin_display.text = 'o  o  o  o  o'
                Clock.schedule_once(
                    lambda dt: setattr(self.err,'text',''), 2)
            return
        else:
            if len(self.pin_entered) < 5:
                self.pin_entered += t
        f = '* ' * len(self.pin_entered)
        e = 'o ' * (5 - len(self.pin_entered))
        self.pin_display.text = (f+e).strip()

    def update_login(self):
        try:
            p = get_profile()
            today = str(datetime.date.today())
            last  = p.get('last_login','')
            streak = p.get('streak', 0)
            if last != today:
                yesterday = str(
                    datetime.date.today() - datetime.timedelta(days=1))
                streak = streak + 1 if last == yesterday else 1
                update_profile(last_login=today, streak=streak)
                if streak >= 7:
                    check_achievements()
            hour = datetime.datetime.now().hour
            if hour >= 0 and hour < 4:
                con = sqlite3.connect(DB)
                c = con.cursor()
                c.execute(
                    "UPDATE achievements SET earned=1,date=? "
                    "WHERE name='Night Owl' AND earned=0", (today,))
                con.commit()
                con.close()
        except:
            pass

# ═══════════════════════════════════════════════════════
#  MAIN SCREEN
# ═══════════════════════════════════════════════════════
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        try:
            if os.path.exists('bg_main.jpg'):
                layout.add_widget(Image(
                    source='bg_main.jpg', allow_stretch=True,
                    keep_ratio=False, size_hint=(1,1),
                    pos_hint={'x':0,'y':0}))
            else:
                bg(layout, C['bg'])
        except:
            bg(layout, C['bg'])

        overlay = FloatLayout(size_hint=(1,1), pos_hint={'x':0,'y':0})
        with overlay.canvas.before:
            Color(0,0,0,0.65)
            overlay._ov = Rectangle(pos=overlay.pos, size=overlay.size)
        overlay.bind(
            pos=lambda i,v: setattr(i._ov,'pos',v),
            size=lambda i,v: setattr(i._ov,'size',v))

        # Header
        header = BoxLayout(pos_hint={'x':0,'top':1},
                           size_hint=(1,0.09), padding=dp(12))
        bg(header, C['header'])
        header.add_widget(lbl('[b]SHADOW MONARCH[/b]', size=16,
                               color=C['purple'], markup=True))
        self.clock_lbl = lbl('', size=12, color=C['sub'],
                              size_hint=(None,1), width=dp(120))
        header.add_widget(self.clock_lbl)
        overlay.add_widget(header)

        # Profile card
        p_card = BoxLayout(orientation='vertical',
            pos_hint={'center_x':0.5,'center_y':0.76},
            size_hint=(0.92, None), height=dp(90),
            padding=dp(10), spacing=dp(4))
        bg(p_card, C['card'], radius=14)

        self.rank_lbl    = lbl('Rank: E', size=13, color=C['gold'], bold=True)
        self.title_lbl   = lbl('Shadow Beginner', size=12, color=C['sub'])
        self.level_lbl   = lbl('Level 1  |  XP: 0', size=12, color=C['text'])
        self.streak_lbl  = lbl('Streak: 0 days', size=11, color=C['green'])
        self.army_lbl    = lbl('Shadow Army: 0', size=11, color=C['purple'])
        self.xp_bar      = ProgressBar(max=100, value=0,
                                        size_hint=(1,None), height=dp(8))

        for w in [self.rank_lbl, self.title_lbl, self.level_lbl,
                  self.streak_lbl, self.army_lbl, self.xp_bar]:
            p_card.add_widget(w)
        overlay.add_widget(p_card)

        # Boss card
        boss_card = BoxLayout(orientation='vertical',
            pos_hint={'center_x':0.5,'center_y':0.58},
            size_hint=(0.92, None), height=dp(65),
            padding=dp(8), spacing=dp(4))
        bg(boss_card, (0.15, 0.0, 0.05, 0.9), radius=12)
        self.boss_lbl = lbl('Daily Boss: Loading...', size=13,
                             color=C['red'], bold=True)
        self.boss_bar = ProgressBar(max=100, value=100,
                                     size_hint=(1,None), height=dp(10))
        boss_card.add_widget(self.boss_lbl)
        boss_card.add_widget(self.boss_bar)
        overlay.add_widget(boss_card)

        # Power bar
        pw_card = BoxLayout(orientation='vertical',
            pos_hint={'center_x':0.5,'center_y':0.46},
            size_hint=(0.92, None), height=dp(45),
            padding=dp(8), spacing=dp(4))
        bg(pw_card, C['card2'], radius=10)
        self.power_lbl = lbl('Power: 100%', size=12, color=C['gold'])
        self.power_bar = ProgressBar(max=100, value=100,
                                      size_hint=(1,None), height=dp(8))
        pw_card.add_widget(self.power_lbl)
        pw_card.add_widget(self.power_bar)
        overlay.add_widget(pw_card)

        # Tools grid
        scroll = ScrollView(pos_hint={'x':0,'y':0.0}, size_hint=(1,0.38))
        grid = GridLayout(cols=2, size_hint_y=None,
                          padding=dp(10), spacing=dp(8))
        grid.bind(minimum_height=grid.setter('height'))

        tools = [
            ('Daily Quests', 'tasks',   C['card'],          '⚔'),
            ('Notes',        'notes',   (0.0,0.08,0.22,0.9),'📝'),
            ('Snippets',     'snippets',(0.0,0.12,0.18,0.9),'💾'),
            ('Calculator',   'calc',    (0.08,0.0,0.2,0.9), '🔢'),
            ('Pomodoro',     'pomodoro',(0.2,0.03,0.05,0.9),'⏱'),
            ('PassGen',      'passgen', (0.0,0.15,0.15,0.9),'🔑'),
            ('Regex',        'regex',   (0.05,0.08,0.2,0.9),'🔍'),
            ('JSON',         'jsonf',   (0.0,0.12,0.2,0.9), '📋'),
            ('Base Conv',    'baseconv',(0.15,0.08,0.0,0.9),'🔄'),
            ('Achievements', 'achieve', (0.12,0.08,0.0,0.9),'🏆'),
            ('Shadow Army',  'army',    (0.1,0.0,0.25,0.9), '👥'),
            ('Skills',       'skills',  (0.05,0.0,0.2,0.9), '⚡'),
        ]

        for name, screen, color, icon in tools:
            btn = styled_btn(f'{icon}\n[b]{name}[/b]',
                color=color, markup=True, font_size=13,
                size_hint_y=None, height=dp(65))
            btn.bind(on_press=lambda x, s=screen: self.go(s))
            grid.add_widget(btn)

        scroll.add_widget(grid)
        overlay.add_widget(scroll)
        layout.add_widget(overlay)
        self.add_widget(layout)

        Clock.schedule_interval(self.update_clock, 1)
        Clock.schedule_once(self.refresh_profile, 0.5)
        Clock.schedule_interval(self.refresh_profile, 30)

    def go(self, screen):
        vibrate_short()
        self.manager.transition = SlideTransition(
            direction='left', duration=0.25)
        self.manager.current = screen

    def update_clock(self, dt):
        try:
            now = datetime.datetime.now()
            self.clock_lbl.text = now.strftime('%H:%M:%S')
        except:
            pass

    def refresh_profile(self, dt=None):
        try:
            p = get_profile()
            self.rank_lbl.text   = f'Rank: {p["rank"]}'
            self.rank_lbl.color  = RANK_COLORS.get(p['rank'], C['gold'])
            self.title_lbl.text  = p['title']
            xp_need = p['level'] * 100
            self.level_lbl.text  = f'Level {p["level"]}  |  XP: {p["xp"]}/{xp_need}'
            self.xp_bar.max      = xp_need
            self.xp_bar.value    = p['xp']
            self.streak_lbl.text = f'Streak: {p["streak"]} days'
            self.army_lbl.text   = f'Shadow Army: {p["army"]}'
            self.power_lbl.text  = f'Power: {p["power"]}%'
            self.power_bar.value = p['power']

            con = sqlite3.connect(DB)
            c = con.cursor()
            today = str(datetime.date.today())
            c.execute('SELECT * FROM boss WHERE id=1')
            boss = c.fetchone()
            if boss:
                if boss[4] != today:
                    bosses = ['Shadow Beast','Dark Phantom',
                              'Void Walker','Night Terror','Abyss Lord']
                    c.execute(
                        'UPDATE boss SET name=?,hp=100,max_hp=100,date=? WHERE id=1',
                        (random.choice(bosses), today))
                    con.commit()
                    c.execute('SELECT * FROM boss WHERE id=1')
                    boss = c.fetchone()
                self.boss_lbl.text  = f'Boss: {boss[1]}  HP:{boss[2]}/{boss[3]}'
                self.boss_bar.max   = boss[3]
                self.boss_bar.value = boss[2]
            con.close()
        except:
            pass

    def on_enter(self):
        self.refresh_profile()

# ═══════════════════════════════════════════════════════
#  TASKS SCREEN
# ═══════════════════════════════════════════════════════
class TasksScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        make_screen_bg(self)

        header = make_header('Daily Quests ⚔',
            back_cb=lambda x: self.go_back())
        layout.add_widget(header)

        self.scroll = ScrollView(
            pos_hint={'x':0,'y':0.15}, size_hint=(1,0.78))
        self.tl = BoxLayout(orientation='vertical', size_hint_y=None,
                            spacing=dp(8), padding=dp(10))
        self.tl.bind(minimum_height=self.tl.setter('height'))
        self.scroll.add_widget(self.tl)
        layout.add_widget(self.scroll)

        inp = BoxLayout(pos_hint={'x':0,'y':0},
                        size_hint=(1,0.14),
                        padding=dp(8), spacing=dp(8))
        self.task_inp = TextInput(
            hint_text='New quest...',
            background_color=C['card2'][:3]+(1,),
            foreground_color=C['text'],
            font_name=DEFAULT_FONT,
            font_size=dp(14), multiline=False)
        add_btn = styled_btn('+', color=C['purple2'],
                             size_hint=(None,1), width=dp(50))
        add_btn.bind(on_press=self.add_task)
        inp.add_widget(self.task_inp)
        inp.add_widget(add_btn)
        layout.add_widget(inp)
        self.add_widget(layout)
        self.refresh()

    def go_back(self):
        self.manager.transition = SlideTransition(
            direction='right', duration=0.25)
        self.manager.current = 'main'

    def refresh(self):
        self.tl.clear_widgets()
        try:
            con = sqlite3.connect(DB)
            c = con.cursor()
            c.execute('SELECT * FROM tasks ORDER BY id DESC')
            tasks = c.fetchall()
            con.close()
            for t in tasks:
                done = t[2]
                row = BoxLayout(size_hint_y=None, height=dp(55),
                                spacing=dp(8), padding=dp(8))
                color = (0.05,0.2,0.05,0.9) if done else C['card']
                bg(row, color, radius=8)
                txt = ('[s]'+t[1]+'[/s]') if done else t[1]
                l = lbl(txt, size=13, markup=True,
                        color=C['green'] if done else C['text'],
                        halign='left',
                        text_size=(Window.width*0.55, None))
                xp_l = lbl(f'+{t[4]}XP', size=10,
                            color=C['gold'], size_hint=(None,1),
                            width=dp(40))
                db = styled_btn('v' if not done else 'o',
                    color=C['green'] if not done else (0.2,0.2,0.2,1),
                    size_hint=(None,1), width=dp(40))
                db.bind(on_press=lambda x,tid=t[0],d=done:
                        self.toggle(tid, d))
                xb = styled_btn('X', color=C['red'][:3]+(0.8,),
                    size_hint=(None,1), width=dp(35))
                xb.bind(on_press=lambda x,tid=t[0]: self.delete(tid))
                row.add_widget(l)
                row.add_widget(xp_l)
                row.add_widget(db)
                row.add_widget(xb)
                self.tl.add_widget(row)
        except:
            pass

    def add_task(self, *a):
        text = self.task_inp.text.strip()
        if text:
            try:
                con = sqlite3.connect(DB)
                c = con.cursor()
                xp = random.randint(10, 30)
                c.execute('INSERT INTO tasks (text,done,date,xp_reward) VALUES (?,0,?,?)',
                          (text, str(datetime.date.today()), xp))
                con.commit()
                con.close()
                self.task_inp.text = ''
                self.refresh()
            except:
                pass

    def toggle(self, tid, done):
        try:
            con = sqlite3.connect(DB)
            c = con.cursor()
            new_done = 0 if done else 1
            c.execute('UPDATE tasks SET done=? WHERE id=?', (new_done, tid))
            if not done:
                c.execute('SELECT xp_reward FROM tasks WHERE id=?', (tid,))
                xp = c.fetchone()
                if xp:
                    add_xp(xp[0])
                    # Damage boss
                    dmg = random.randint(10, 25)
                    c.execute('UPDATE boss SET hp=MAX(0,hp-?) WHERE id=1', (dmg,))
                    c.execute('SELECT hp FROM boss WHERE id=1')
                    hp = c.fetchone()
                    if hp and hp[0] == 0:
                        today = str(datetime.date.today())
                        c.execute(
                            "UPDATE achievements SET earned=1,date=? "
                            "WHERE name='Boss Slayer' AND earned=0", (today,))
                    send_notification('Quest Complete!',
                                      f'+{xp[0]} XP earned!')
                    vibrate_short()
            con.commit()
            con.close()
            self.refresh()
            # Refresh main
            try:
                self.manager.get_screen('main').refresh_profile()
            except:
                pass
        except:
            pass

    def delete(self, tid):
        try:
            con = sqlite3.connect(DB)
            c = con.cursor()
            c.execute('DELETE FROM tasks WHERE id=?', (tid,))
            con.commit()
            con.close()
            self.refresh()
        except:
            pass

# ═══════════════════════════════════════════════════════
#  NOTES SCREEN
# ═══════════════════════════════════════════════════════
class NotesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        make_screen_bg(self)
        layout.add_widget(make_header('Notes 📝',
            back_cb=lambda x: self.go_back()))

        self.scroll = ScrollView(
            pos_hint={'x':0,'y':0.18}, size_hint=(1,0.75))
        self.nl = BoxLayout(orientation='vertical', size_hint_y=None,
                            spacing=dp(8), padding=dp(10))
        self.nl.bind(minimum_height=self.nl.setter('height'))
        self.scroll.add_widget(self.nl)
        layout.add_widget(self.scroll)

        inp = BoxLayout(pos_hint={'x':0,'y':0},
                        size_hint=(1,0.17), padding=dp(8), spacing=dp(8))
        self.note_inp = TextInput(
            hint_text='Write a note...',
            background_color=C['card2'][:3]+(1,),
            foreground_color=C['text'],
            font_name=DEFAULT_FONT, font_size=dp(14))
        add_btn = styled_btn('+', color=C['purple2'],
                             size_hint=(None,1), width=dp(50))
        add_btn.bind(on_press=self.add_note)
        inp.add_widget(self.note_inp)
        inp.add_widget(add_btn)
        layout.add_widget(inp)
        self.add_widget(layout)
        self.refresh()

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.25)
        self.manager.current = 'main'

    def refresh(self):
        self.nl.clear_widgets()
        try:
            con = sqlite3.connect(DB)
            c = con.cursor()
            c.execute('SELECT * FROM notes ORDER BY id DESC')
            notes = c.fetchall()
            con.close()
            for n in notes:
                row = BoxLayout(size_hint_y=None, height=dp(60),
                                spacing=dp(8), padding=dp(6))
                bg(row, C['card'], radius=8)
                l = lbl(n[1][:60]+('...' if len(n[1])>60 else ''),
                        size=13, halign='left',
                        text_size=(Window.width*0.6, None))
                xb = styled_btn('X', color=C['red'][:3]+(0.8,),
                    size_hint=(None,1), width=dp(40))
                xb.bind(on_press=lambda x,nid=n[0]: self.delete(nid))
                row.add_widget(l)
                row.add_widget(xb)
                self.nl.add_widget(row)
        except:
            pass

    def add_note(self, *a):
        text = self.note_inp.text.strip()
        if text:
            try:
                con = sqlite3.connect(DB)
                c = con.cursor()
                c.execute('INSERT INTO notes (text,time) VALUES (?,?)',
                          (text, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))))
                con.commit()
                con.close()
                self.note_inp.text = ''
                self.refresh()
            except:
                pass

    def delete(self, nid):
        try:
            con = sqlite3.connect(DB)
            c = con.cursor()
            c.execute('DELETE FROM notes WHERE id=?', (nid,))
            con.commit()
            con.close()
            self.refresh()
        except:
            pass

# ═══════════════════════════════════════════════════════
#  SNIPPETS SCREEN
# ═══════════════════════════════════════════════════════
class SnippetsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        make_screen_bg(self)
        layout.add_widget(make_header('Code Snippets 💾',
            back_cb=lambda x: self.go_back()))

        self.scroll = ScrollView(
            pos_hint={'x':0,'y':0.25}, size_hint=(1,0.68))
        self.sl = BoxLayout(orientation='vertical', size_hint_y=None,
                            spacing=dp(8), padding=dp(10))
        self.sl.bind(minimum_height=self.sl.setter('height'))
        self.scroll.add_widget(self.sl)
        layout.add_widget(self.scroll)

        inp = BoxLayout(orientation='vertical',
                        pos_hint={'x':0,'y':0},
                        size_hint=(1,0.24),
                        padding=dp(8), spacing=dp(6))
        self.t_inp = TextInput(hint_text='Title...',
            multiline=False,
            background_color=C['card2'][:3]+(1,),
            foreground_color=C['text'],
            font_name=DEFAULT_FONT,
            size_hint_y=None, height=dp(38), font_size=dp(13))
        self.c_inp = TextInput(hint_text='Code here...',
            background_color=(0.03,0.0,0.1,1),
            foreground_color=(0.4,1,0.4,1),
            font_name=DEFAULT_FONT, font_size=dp(12))
        sb = styled_btn('Save Snippet', color=C['purple2'],
                        size_hint_y=None, height=dp(35))
        sb.bind(on_press=self.add_snip)
        inp.add_widget(self.t_inp)
        inp.add_widget(self.c_inp)
        inp.add_widget(sb)
        layout.add_widget(inp)
        self.add_widget(layout)
        self.refresh()

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.25)
        self.manager.current = 'main'

    def refresh(self):
        self.sl.clear_widgets()
        try:
            con = sqlite3.connect(DB)
            c = con.cursor()
            c.execute('SELECT * FROM snippets ORDER BY id DESC')
            snips = c.fetchall()
            con.close()
            for s in snips:
                card = BoxLayout(size_hint_y=None, height=dp(70),
                                 spacing=dp(8), padding=dp(8))
                bg(card, C['card2'], radius=8)
                info = BoxLayout(orientation='vertical')
                info.add_widget(lbl(s[1], size=13, bold=True,
                                    color=C['purple'], halign='left'))
                info.add_widget(lbl(s[2][:40]+'...', size=11,
                                    color=(0.4,1,0.4,1), halign='left'))
                cb = styled_btn('Copy', color=(0,0.35,0.15,1),
                    size_hint=(None,1), width=dp(55))
                cb.bind(on_press=lambda x,code=s[2]: Clipboard.copy(code))
                xb = styled_btn('X', color=C['red'][:3]+(0.8,),
                    size_hint=(None,1), width=dp(35))
                xb.bind(on_press=lambda x,sid=s[0]: self.delete(sid))
                card.add_widget(info)
                card.add_widget(cb)
                card.add_widget(xb)
                self.sl.add_widget(card)
        except:
            pass

    def add_snip(self, *a):
        t = self.t_inp.text.strip()
        c = self.c_inp.text.strip()
        if t and c:
            try:
                con = sqlite3.connect(DB)
                cur = con.cursor()
                cur.execute('INSERT INTO snippets (title,code) VALUES (?,?)', (t,c))
                con.commit()
                # Check achievement
                cur.execute('SELECT COUNT(*) FROM snippets')
                cnt = cur.fetchone()[0]
                if cnt >= 10:
                    today = str(datetime.date.today())
                    cur.execute(
                        "UPDATE achievements SET earned=1,date=? "
                        "WHERE name='Code Keeper' AND earned=0", (today,))
                    con.commit()
                con.close()
                self.t_inp.text = ''
                self.c_inp.text = ''
                self.refresh()
            except:
                pass

    def delete(self, sid):
        try:
            con = sqlite3.connect(DB)
            c = con.cursor()
            c.execute('DELETE FROM snippets WHERE id=?', (sid,))
            con.commit()
            con.close()
            self.refresh()
        except:
            pass

# ═══════════════════════════════════════════════════════
#  CALCULATOR
# ═══════════════════════════════════════════════════════
class CalcScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.expr = ''
        layout = FloatLayout()
        make_screen_bg(self)
        layout.add_widget(make_header('Dev Calculator 🔢',
            back_cb=lambda x: self.go_back()))

        self.disp = lbl('0', size=30, color=C['text'],
            pos_hint={'center_x':0.5,'center_y':0.79},
            size_hint=(0.92,None), height=dp(55), halign='right')
        self.sub  = lbl('', size=12, color=C['sub'],
            pos_hint={'center_x':0.5,'center_y':0.71},
            size_hint=(0.92,None), height=dp(22), halign='right')
        layout.add_widget(self.disp)
        layout.add_widget(self.sub)

        grid = GridLayout(cols=4,
            pos_hint={'center_x':0.5,'center_y':0.36},
            size_hint=(0.95,0.54), spacing=dp(6))
        btns = [
            ('C',(0.4,0.0,0.1,1)),('()',(0.2,0.0,0.4,1)),
            ('%',(0.2,0.0,0.4,1)),('/',(0.35,0.0,0.7,1)),
            ('7',None),('8',None),('9',None),('*',(0.35,0.0,0.7,1)),
            ('4',None),('5',None),('6',None),('-',(0.35,0.0,0.7,1)),
            ('1',None),('2',None),('3',None),('+',(0.35,0.0,0.7,1)),
            ('HEX',(0,0.2,0.4,1)),('0',None),('.',None),
            ('=',(0.5,0.0,0.9,1)),
        ]
        for t, col in btns:
            b = styled_btn(t, color=col if col else C['card'], font_size=16)
            b.bind(on_press=self.on_calc)
            grid.add_widget(b)
        layout.add_widget(grid)
        self.add_widget(layout)

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.25)
        self.manager.current = 'main'

    def on_calc(self, btn):
        t = btn.text
        vibrate_short()
        if t == 'C':
            self.expr = ''
            self.disp.text = '0'
            self.sub.text  = ''
        elif t == '=':
            try:
                r = eval(self.expr)
                self.sub.text  = self.expr
                self.disp.text = str(r)
                self.expr = str(r)
            except:
                self.disp.text = 'Error'
                self.expr = ''
        elif t == 'HEX':
            try:
                v = int(eval(self.expr))
                self.sub.text = f'HEX:{hex(v)}  BIN:{bin(v)}  OCT:{oct(v)}'
            except:
                self.sub.text = 'Not integer'
        elif t == '()':
            self.expr += '('
            self.disp.text = self.expr
        else:
            self.expr += t
            self.disp.text = self.expr

# ═══════════════════════════════════════════════════════
#  POMODORO
# ═══════════════════════════════════════════════════════
class PomodoroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.seconds_left = 25*60
        self.running = False
        self.is_break = False
        self.sessions = 0
        self._clock = None
        layout = FloatLayout()
        make_screen_bg(self)
        layout.add_widget(make_header('Pomodoro Timer ⏱',
            back_cb=lambda x: self.go_back()))

        self.mode_lbl = lbl('FOCUS', size=16, color=C['red'], bold=True,
            pos_hint={'center_x':0.5,'center_y':0.78},
            size_hint=(1,None), height=dp(25))
        self.timer_lbl = lbl('25:00', size=60, color=C['text'], bold=True,
            pos_hint={'center_x':0.5,'center_y':0.65},
            size_hint=(1,None), height=dp(80))
        self.sess_lbl = lbl('Sessions: 0', size=13, color=C['sub'],
            pos_hint={'center_x':0.5,'center_y':0.54},
            size_hint=(1,None), height=dp(25))

        btns = BoxLayout(pos_hint={'center_x':0.5,'center_y':0.42},
                         size_hint=(0.8,None), height=dp(55), spacing=dp(12))
        self.start_btn = styled_btn('START', color=C['green'][:3]+(1,), font_size=18)
        self.start_btn.bind(on_press=self.toggle)
        reset_btn = styled_btn('RESET', color=C['red'][:3]+(0.8,), font_size=18)
        reset_btn.bind(on_press=self.reset)
        btns.add_widget(self.start_btn)
        btns.add_widget(reset_btn)

        for w in [self.mode_lbl, self.timer_lbl, self.sess_lbl, btns]:
            layout.add_widget(w)
        self.add_widget(layout)

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.25)
        self.manager.current = 'main'

    def toggle(self, *a):
        if self.running:
            self.running = False
            if self._clock: self._clock.cancel()
            self.start_btn.text = 'START'
        else:
            self.running = True
            self._clock = Clock.schedule_interval(self.tick, 1)
            self.start_btn.text = 'PAUSE'

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
                send_notification('Focus Complete!', 'Take a 5min break!')
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

# ═══════════════════════════════════════════════════════
#  PASSWORD GENERATOR
# ═══════════════════════════════════════════════════════
class PassGenScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        make_screen_bg(self)
        layout.add_widget(make_header('Password Generator 🔑',
            back_cb=lambda x: self.go_back()))

        self.result = lbl('Press Generate', size=16,
            color=(0.5,1,0.5,1),
            pos_hint={'center_x':0.5,'center_y':0.72},
            size_hint=(0.9,None), height=dp(45), halign='center')
        self.len_lbl = lbl('Length: 16', size=14, color=C['text'],
            pos_hint={'center_x':0.5,'center_y':0.60},
            size_hint=(1,None), height=dp(25))
        self.slider = Slider(min=8, max=32, value=16, step=1,
            pos_hint={'center_x':0.5,'center_y':0.52},
            size_hint=(0.85,None), height=dp(40))
        self.slider.bind(value=lambda s,v: setattr(
            self.len_lbl, 'text', f'Length: {int(v)}'))

        self.inc_upper   = True
        self.inc_digits  = True
        self.inc_symbols = True

        opts = BoxLayout(pos_hint={'center_x':0.5,'center_y':0.41},
                         size_hint=(0.85,None), height=dp(40), spacing=dp(8))
        self.bu = styled_btn('ABC', color=C['purple2'], font_size=13)
        self.bd = styled_btn('123', color=C['purple2'], font_size=13)
        self.bs = styled_btn('#@!', color=C['purple2'], font_size=13)
        self.bu.bind(on_press=lambda x: self.tog('u'))
        self.bd.bind(on_press=lambda x: self.tog('d'))
        self.bs.bind(on_press=lambda x: self.tog('s'))
        opts.add_widget(self.bu)
        opts.add_widget(self.bd)
        opts.add_widget(self.bs)

        gen = styled_btn('GENERATE', color=C['purple2'], font_size=17,
            size_hint=(0.6,None), height=dp(50),
            pos_hint={'center_x':0.5,'center_y':0.28})
        gen.bind(on_press=self.generate)
        copy = styled_btn('Copy', color=(0,0.35,0.15,1), font_size=14,
            size_hint=(0.5,None), height=dp(40),
            pos_hint={'center_x':0.5,'center_y':0.18})
        copy.bind(on_press=lambda x: Clipboard.copy(self.result.text))

        for w in [self.result, self.len_lbl, self.slider,
                  opts, gen, copy]:
            layout.add_widget(w)
        self.add_widget(layout)

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.25)
        self.manager.current = 'main'

    def tog(self, opt):
        if opt == 'u':
            self.inc_upper = not self.inc_upper
            self.bu.color = C['green'] if self.inc_upper else C['sub']
        elif opt == 'd':
            self.inc_digits = not self.inc_digits
            self.bd.color = C['green'] if self.inc_digits else C['sub']
        elif opt == 's':
            self.inc_symbols = not self.inc_symbols
            self.bs.color = C['green'] if self.inc_symbols else C['sub']

    def generate(self, *a):
        chars = string.ascii_lowercase
        if self.inc_upper:   chars += string.ascii_uppercase
        if self.inc_digits:  chars += string.digits
        if self.inc_symbols: chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
        l = int(self.slider.value)
        self.result.text = ''.join(random.choice(chars) for _ in range(l))

# ═══════════════════════════════════════════════════════
#  REGEX TESTER
# ═══════════════════════════════════════════════════════
class RegexScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        make_screen_bg(self)
        layout.add_widget(make_header('Regex Tester 🔍',
            back_cb=lambda x: self.go_back()))

        content = BoxLayout(orientation='vertical',
            pos_hint={'x':0,'y':0}, size_hint=(1,0.93),
            padding=dp(10), spacing=dp(8))
        content.add_widget(lbl('Pattern:', size=13, color=C['purple'],
                                size_hint_y=None, height=dp(22), halign='left'))
        self.pat = TextInput(hint_text='e.g. \\d+',
            multiline=False,
            background_color=C['card2'][:3]+(1,),
            foreground_color=(1,1,0,1),
            font_name=DEFAULT_FONT,
            font_size=dp(14), size_hint_y=None, height=dp(42))
        content.add_widget(self.pat)
        content.add_widget(lbl('Test String:', size=13, color=C['purple'],
                                size_hint_y=None, height=dp(22), halign='left'))
        self.test = TextInput(hint_text='Text to test...',
            background_color=C['card2'][:3]+(1,),
            foreground_color=C['text'],
            font_name=DEFAULT_FONT,
            font_size=dp(13), size_hint_y=None, height=dp(80))
        content.add_widget(self.test)
        tb = styled_btn('TEST', color=C['purple2'], font_size=16,
                        size_hint_y=None, height=dp(45))
        tb.bind(on_press=self.test_regex)
        content.add_widget(tb)
        self.res = lbl('', size=13, color=C['green'], halign='left',
                        text_size=(Window.width-dp(20), None))
        content.add_widget(self.res)
        layout.add_widget(content)
        self.add_widget(layout)

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.25)
        self.manager.current = 'main'

    def test_regex(self, *a):
        try:
            m = re.findall(self.pat.text, self.test.text)
            if m:
                self.res.color = C['green']
                self.res.text = f'Found {len(m)}:\n' + '\n'.join(str(x) for x in m[:10])
            else:
                self.res.color = C['red']
                self.res.text = 'No matches'
        except Exception as e:
            self.res.color = C['gold']
            self.res.text  = f'Error: {e}'

# ═══════════════════════════════════════════════════════
#  JSON FORMATTER
# ═══════════════════════════════════════════════════════
class JsonScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        make_screen_bg(self)
        layout.add_widget(make_header('JSON Formatter 📋',
            back_cb=lambda x: self.go_back()))

        content = BoxLayout(orientation='vertical',
            pos_hint={'x':0,'y':0}, size_hint=(1,0.93),
            padding=dp(10), spacing=dp(8))
        self.inp = TextInput(hint_text='Paste JSON...',
            background_color=(0.03,0.0,0.1,1),
            foreground_color=C['text'],
            font_name=DEFAULT_FONT, font_size=dp(12))
        btns = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(8))
        for txt, cb, col in [
            ('Format',   self.fmt, C['purple2']),
            ('Validate', self.val, (0,0.3,0.15,1)),
            ('Copy',     lambda x: Clipboard.copy(self.inp.text), (0.2,0.1,0,1))
        ]:
            b = styled_btn(txt, color=col, font_size=15)
            b.bind(on_press=cb)
            btns.add_widget(b)
        self.status = lbl('', size=13, color=C['green'],
                          size_hint_y=None, height=dp(30))
        content.add_widget(self.inp)
        content.add_widget(btns)
        content.add_widget(self.status)
        layout.add_widget(content)
        self.add_widget(layout)

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.25)
        self.manager.current = 'main'

    def fmt(self, *a):
        try:
            self.inp.text = json.dumps(
                json.loads(self.inp.text), indent=2, ensure_ascii=False)
            self.status.color = C['green']
            self.status.text  = 'Formatted!'
        except Exception as e:
            self.status.color = C['red']
            self.status.text  = f'Error: {e}'

    def val(self, *a):
        try:
            json.loads(self.inp.text)
            self.status.color = C['green']
            self.status.text  = 'Valid JSON!'
        except Exception as e:
            self.status.color = C['red']
            self.status.text  = f'Invalid: {e}'

# ═══════════════════════════════════════════════════════
#  BASE CONVERTER
# ═══════════════════════════════════════════════════════
class BaseConvScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        make_screen_bg(self)
        layout.add_widget(make_header('Base Converter 🔄',
            back_cb=lambda x: self.go_back()))

        content = BoxLayout(orientation='vertical',
            pos_hint={'x':0,'y':0}, size_hint=(1,0.93),
            padding=dp(15), spacing=dp(10))
        self.fields = {}
        for label, key, color in [
            ('Decimal',     'dec', C['text']),
            ('Hexadecimal', 'hex', (1,0.8,0,1)),
            ('Binary',      'bin', (0.4,1,0.4,1)),
            ('Octal',       'oct', (0.6,0.8,1,1)),
        ]:
            content.add_widget(lbl(label, size=13, color=C['purple'],
                                    size_hint_y=None, height=dp(20), halign='left'))
            inp = TextInput(multiline=False,
                background_color=C['card2'][:3]+(1,),
                foreground_color=color,
                font_name=DEFAULT_FONT,
                font_size=dp(14), size_hint_y=None, height=dp(42))
            self.fields[key] = inp
            content.add_widget(inp)

        cb = styled_btn('CONVERT', color=C['purple2'], font_size=17,
                        size_hint_y=None, height=dp(50))
        cb.bind(on_press=self.convert)
        content.add_widget(cb)
        layout.add_widget(content)
        self.add_widget(layout)

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.25)
        self.manager.current = 'main'

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
        except:
            f['dec'].text = 'Error'

# ═══════════════════════════════════════════════════════
#  ACHIEVEMENTS
# ═══════════════════════════════════════════════════════
class AchieveScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        make_screen_bg(self)
        layout.add_widget(make_header('Achievements 🏆',
            back_cb=lambda x: self.go_back()))

        self.scroll = ScrollView(
            pos_hint={'x':0,'y':0}, size_hint=(1,0.93))
        self.al = BoxLayout(orientation='vertical', size_hint_y=None,
                            spacing=dp(8), padding=dp(10))
        self.al.bind(minimum_height=self.al.setter('height'))
        self.scroll.add_widget(self.al)
        layout.add_widget(self.scroll)
        self.add_widget(layout)

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.25)
        self.manager.current = 'main'

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
                card = BoxLayout(size_hint_y=None, height=dp(65),
                                 spacing=dp(8), padding=dp(10))
                bg(card,
                   (0.05,0.15,0.05,0.9) if earned else C['card'],
                   radius=10)
                info = BoxLayout(orientation='vertical')
                info.add_widget(lbl(
                    ('✅ ' if earned else '🔒 ') + a[1],
                    size=14, bold=True,
                    color=C['gold'] if earned else C['sub'],
                    halign='left'))
                info.add_widget(lbl(a[2], size=11,
                    color=C['text'], halign='left'))
                if earned and a[4]:
                    info.add_widget(lbl(f'Earned: {a[4]}', size=10,
                        color=C['green'], halign='left'))
                card.add_widget(info)
                self.al.add_widget(card)
        except:
            pass

# ═══════════════════════════════════════════════════════
#  SHADOW ARMY
# ═══════════════════════════════════════════════════════
class ArmyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        make_screen_bg(self)
        layout.add_widget(make_header('Shadow Army 👥',
            back_cb=lambda x: self.go_back()))

        self.info = BoxLayout(orientation='vertical',
            pos_hint={'center_x':0.5,'center_y':0.6},
            size_hint=(0.85, None), height=dp(200),
            padding=dp(15), spacing=dp(10))
        bg(self.info, C['card'], radius=14)

        self.army_lbl   = lbl('Army: 0', size=28, color=C['purple'], bold=True)
        self.rank_lbl   = lbl('Rank: E', size=18, color=C['gold'])
        self.level_lbl  = lbl('Level: 1', size=16, color=C['text'])
        self.streak_lbl = lbl('Streak: 0 days', size=14, color=C['green'])
        self.id_lbl     = lbl('Shadow ID: ...', size=12, color=C['sub'])

        self.xp_bar = ProgressBar(max=100, value=0,
                                   size_hint=(1,None), height=dp(12))

        for w in [self.army_lbl, self.rank_lbl, self.level_lbl,
                  self.streak_lbl, self.id_lbl, self.xp_bar]:
            self.info.add_widget(w)
        layout.add_widget(self.info)

        next_lbl = lbl('Next Rank Requirements:', size=13,
            color=C['purple'],
            pos_hint={'center_x':0.5,'center_y':0.28},
            size_hint=(0.85,None), height=dp(25))
        self.next_info = lbl('', size=12, color=C['text'],
            pos_hint={'center_x':0.5,'center_y':0.21},
            size_hint=(0.85,None), height=dp(45), halign='center')
        layout.add_widget(next_lbl)
        layout.add_widget(self.next_info)
        self.add_widget(layout)

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.25)
        self.manager.current = 'main'

    def on_enter(self):
        try:
            p = get_profile()
            self.army_lbl.text   = f'Shadow Army: {p["army"]}'
            self.rank_lbl.text   = f'Rank: {p["rank"]}'
            self.rank_lbl.color  = RANK_COLORS.get(p['rank'], C['gold'])
            self.level_lbl.text  = f'Level: {p["level"]}'
            self.streak_lbl.text = f'Streak: {p["streak"]} days'
            self.id_lbl.text     = f'Shadow ID: {p["shadow_id"]}'
            xp_need = p['level'] * 100
            self.xp_bar.max   = xp_need
            self.xp_bar.value = p['xp']
            next_ranks = {
                'E': 'Reach Level 5 → Rank D',
                'D': 'Reach Level 10 → Rank C',
                'C': 'Reach Level 20 → Rank B',
                'B': 'Reach Level 35 → Rank A',
                'A': 'Reach Level 50 → Rank S',
                'S': 'Maximum Rank Achieved!'
            }
            self.next_info.text = next_ranks.get(p['rank'], '')
        except:
            pass

# ═══════════════════════════════════════════════════════
#  SKILLS
# ═══════════════════════════════════════════════════════
class SkillsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        make_screen_bg(self)
        layout.add_widget(make_header('Skill Inventory ⚡',
            back_cb=lambda x: self.go_back()))

        self.scroll = ScrollView(
            pos_hint={'x':0,'y':0}, size_hint=(1,0.93))
        self.sl = BoxLayout(orientation='vertical', size_hint_y=None,
                            spacing=dp(8), padding=dp(10))
        self.sl.bind(minimum_height=self.sl.setter('height'))
        self.scroll.add_widget(self.sl)
        layout.add_widget(self.scroll)
        self.add_widget(layout)

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.25)
        self.manager.current = 'main'

    def on_enter(self):
        self.sl.clear_widgets()
        try:
            p = get_profile()
            rank = p['rank']
            level = p['level']
            skills = [
                ('Shadow Step',    'E', 1,  'Basic movement in darkness'),
                ('Shadow Cloak',   'E', 3,  'Become invisible to distractions'),
                ('Dark Vision',    'D', 5,  'See opportunities others miss'),
                ('Shadow Army',    'D', 8,  'Command your task army'),
                ('Void Strike',    'C', 12, 'Eliminate tasks instantly'),
                ('Shadow Domain',  'C', 18, 'Control your environment'),
                ('Monarch\'s Will','B', 25, 'Bend reality to your goals'),
                ('Arise!',         'A', 40, 'Summon maximum productivity'),
                ('Shadow Monarch', 'S', 50, 'Ultimate power unlocked'),
            ]
            rank_order = ['E','D','C','B','A','S']
            for name, req_rank, req_level, desc in skills:
                unlocked = (rank_order.index(rank) >=
                           rank_order.index(req_rank) and
                           level >= req_level)
                card = BoxLayout(size_hint_y=None, height=dp(70),
                                 spacing=dp(8), padding=dp(10))
                bg(card,
                   (0.05,0.12,0.05,0.9) if unlocked else C['card2'],
                   radius=10)
                info = BoxLayout(orientation='vertical')
                info.add_widget(lbl(
                    ('⚡ ' if unlocked else '🔒 ') + name,
                    size=14, bold=True,
                    color=C['gold'] if unlocked else C['sub'],
                    halign='left'))
                info.add_widget(lbl(desc, size=11,
                    color=C['text'], halign='left'))
                req = lbl(f'Req: Rank {req_rank} | Lv {req_level}',
                    size=10, color=C['green'] if unlocked else C['red'],
                    size_hint=(None,1), width=dp(120))
                card.add_widget(info)
                card.add_widget(req)
                self.sl.add_widget(card)
        except:
            pass

# ═══════════════════════════════════════════════════════
#  APP
# ═══════════════════════════════════════════════════════
class ShadowMonarchApp(App):
    def build(self):
        try:
            Window.clearcolor = (0,0,0,1)
            init_db()
            sm = ScreenManager(transition=FadeTransition(duration=0.3))
            sm.add_widget(SplashScreen(name='splash'))
            sm.add_widget(LockScreen(name='lock'))
            sm.add_widget(MainScreen(name='main'))
            sm.add_widget(TasksScreen(name='tasks'))
            sm.add_widget(NotesScreen(name='notes'))
            sm.add_widget(SnippetsScreen(name='snippets'))
            sm.add_widget(CalcScreen(name='calc'))
            sm.add_widget(PomodoroScreen(name='pomodoro'))
            sm.add_widget(PassGenScreen(name='passgen'))
            sm.add_widget(RegexScreen(name='regex'))
            sm.add_widget(JsonScreen(name='jsonf'))
            sm.add_widget(BaseConvScreen(name='baseconv'))
            sm.add_widget(AchieveScreen(name='achieve'))
            sm.add_widget(ArmyScreen(name='army'))
            sm.add_widget(SkillsScreen(name='skills'))
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
