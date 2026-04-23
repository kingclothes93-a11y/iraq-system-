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
import math

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
from kivy.core.text import LabelBase
from kivy.utils import platform

try:
    from plyer import notification, vibrator
    PLYER_OK = True
except Exception:
    PLYER_OK = False

Logger.setLevel('DEBUG')

# ── Font ──────────────────────────────────────────────
FONT = 'font.ttf'
if os.path.exists(FONT):
    try:
        LabelBase.register(name='AppFont', fn_regular=FONT)
        DEFAULT_FONT = 'AppFont'
    except Exception:
        DEFAULT_FONT = 'Roboto'
else:
    DEFAULT_FONT = 'Roboto'

# ── Arabic reshaper ───────────────────────────────────
def ar(text):
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(str(text)))
    except Exception:
        return str(text)

# ── Colors ────────────────────────────────────────────
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
    'blue':    (0.0,  0.5,  1.0,  1),
    'cyan':    (0.0,  0.8,  0.9,  1),
    'orange':  (1.0,  0.5,  0.0,  1),
    'pink':    (1.0,  0.2,  0.6,  1),
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
        title TEXT DEFAULT 'مبتدئ الظل',
        army INTEGER DEFAULT 0,
        power INTEGER DEFAULT 100
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        done INTEGER DEFAULT 0,
        date TEXT,
        xp_reward INTEGER DEFAULT 10,
        priority INTEGER DEFAULT 1
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

    c.execute('SELECT COUNT(*) FROM profile')
    if c.fetchone()[0] == 0:
        sid = 'SM-' + hashlib.md5(
            str(datetime.datetime.now()).encode()).hexdigest()[:8].upper()
        c.execute(
            'INSERT INTO profile '
            '(shadow_id,level,xp,rank,streak,last_login,title,army,power) '
            'VALUES (?,1,0,"E",0,?,"مبتدئ الظل",0,100)',
            (sid, str(datetime.date.today())))

    c.execute('SELECT COUNT(*) FROM achievements')
    if c.fetchone()[0] == 0:
        achs = [
            ('اول_ظل',        'أكمل مهمتك الأولى',            0, ''),
            ('جيش_x10',       'أكمل 10 مهام',                 0, ''),
            ('جيش_x50',       'أكمل 50 مهمة',                 0, ''),
            ('محارب_اسبوع',   'حافظ على سلسلة 7 أيام',        0, ''),
            ('سيد_الظل',      'ابلغ رتبة S',                   0, ''),
            ('حارس_الكود',    'احفظ 10 مقتطفات كود',           0, ''),
            ('بومة_الليل',    'سجّل الدخول بعد منتصف الليل',  0, ''),
            ('قاتل_الرئيس',   'اهزم الرئيس اليومي',            0, ''),
        ]
        c.executemany(
            'INSERT INTO achievements (name,desc,earned,date) VALUES (?,?,?,?)', achs)

    c.execute('SELECT COUNT(*) FROM boss')
    if c.fetchone()[0] == 0:
        bosses = ['وحش الظل', 'الشبح الداكن', 'سالك الفراغ',
                  'رعب الليل', 'رب الهاوية']
        c.execute(
            'INSERT INTO boss (id,name,hp,max_hp,date) VALUES (1,?,100,100,?)',
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
            return {
                'shadow_id': row[1], 'level': row[2], 'xp': row[3],
                'rank': row[4], 'streak': row[5], 'last_login': row[6],
                'title': row[7], 'army': row[8], 'power': row[9]
            }
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
    xp    = p.get('xp', 0) + amount
    level = p.get('level', 1)
    rank  = p.get('rank', 'E')
    army  = p.get('army', 0) + 1

    xp_needed = level * 100
    while xp >= xp_needed:
        xp       -= xp_needed
        level    += 1
        xp_needed = level * 100

    ranks  = {1: 'E', 5: 'D', 10: 'C', 20: 'B', 35: 'A', 50: 'S'}
    titles = {
        'E': 'مبتدئ الظل',
        'D': 'سالك الظل',
        'C': 'فارس الظل',
        'B': 'صائد الظل',
        'A': 'سيد الظل',
        'S': 'ملك الظل',
    }
    for lvl, r in sorted(ranks.items()):
        if level >= lvl:
            rank = r
    title = titles.get(rank, p.get('title', 'مبتدئ الظل'))
    update_profile(xp=xp, level=level, rank=rank, title=title, army=army)
    check_achievements(army=army, rank=rank)


def check_achievements(army=0, rank='E'):
    try:
        con   = sqlite3.connect(DB)
        c     = con.cursor()
        today = str(datetime.date.today())
        if army >= 1:
            c.execute("UPDATE achievements SET earned=1,date=? WHERE name='اول_ظل' AND earned=0", (today,))
        if army >= 10:
            c.execute("UPDATE achievements SET earned=1,date=? WHERE name='جيش_x10' AND earned=0", (today,))
        if army >= 50:
            c.execute("UPDATE achievements SET earned=1,date=? WHERE name='جيش_x50' AND earned=0", (today,))
        if rank == 'S':
            c.execute("UPDATE achievements SET earned=1,date=? WHERE name='سيد_الظل' AND earned=0", (today,))
        con.commit()
        con.close()
    except Exception:
        pass


# ── UI Helpers ────────────────────────────────────────
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


def styled_btn(text, color=None, fg=(1, 1, 1, 1), radius=10,
               font_size=15, markup=False, **kwargs):
    if color is None:
        color = C['purple2']
    btn = Button(
        text=text, markup=markup,
        font_size=dp(font_size), font_name=DEFAULT_FONT,
        background_color=(0, 0, 0, 0), color=fg,
        background_normal='', **kwargs)
    with btn.canvas.before:
        Color(*color)
        btn._bg = RoundedRectangle(
            pos=btn.pos, size=btn.size, radius=[dp(radius)])
    btn.bind(
        pos=lambda i, v: setattr(i._bg, 'pos', v),
        size=lambda i, v: setattr(i._bg, 'size', v))
    return btn


def lbl(text, size=14, color=None, bold=False,
        halign='center', markup=False, **kwargs):
    if color is None:
        color = C['text']
    return Label(
        text=text, font_size=dp(size), font_name=DEFAULT_FONT,
        color=color, bold=bold, halign=halign, markup=markup, **kwargs)


def make_screen_bg(screen):
    with screen.canvas.before:
        Color(*C['bg'])
        screen._bg = Rectangle(pos=screen.pos, size=screen.size)
    screen.bind(
        pos=lambda i, v: setattr(i._bg, 'pos', v),
        size=lambda i, v: setattr(i._bg, 'size', v))


def make_header(title, back_cb=None):
    header = BoxLayout(
        pos_hint={'x': 0, 'top': 1},
        size_hint=(1, 0.08), padding=dp(10))
    bg(header, C['header'])
    if back_cb:
        b = styled_btn(ar('رجوع'), color=(0, 0, 0, 0),
                       fg=C['purple'], size_hint=(None, 1), width=dp(80))
        b.bind(on_press=back_cb)
        header.add_widget(b)
    header.add_widget(lbl(title, size=16, color=C['purple']))
    return header


def go_back(manager, target='main'):
    manager.transition = SlideTransition(direction='right', duration=0.25)
    manager.current = target


def vibrate_short():
    try:
        if PLYER_OK and platform == 'android':
            vibrator.vibrate(0.05)
    except Exception:
        pass


def send_notification(title_text, msg):
    try:
        if PLYER_OK:
            notification.notify(title=title_text, message=msg, timeout=3)
    except Exception:
        pass


RANK_COLORS = {
    'E': (0.5, 0.5, 0.5, 1),
    'D': (0.2, 0.6, 0.2, 1),
    'C': (0.2, 0.4, 0.9, 1),
    'B': (0.6, 0.2, 0.9, 1),
    'A': (1.0, 0.5, 0.0, 1),
    'S': (1.0, 0.8, 0.0, 1),
}

# ══════════════════════════════════════════════════════
#  SPLASH SCREEN
# ══════════════════════════════════════════════════════
class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        bg(root, C['bg'])
        root.add_widget(lbl(
            ar('شادو مونارك'), size=40, color=C['purple'], bold=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.62},
            size_hint=(1, None), height=dp(65)))
        root.add_widget(lbl(
            'Shadow Monarch v3.0', size=14, color=C['sub'],
            pos_hint={'center_x': 0.5, 'center_y': 0.51},
            size_hint=(1, None), height=dp(28)))
        root.add_widget(lbl(
            ar('استيقظ...'), size=13, color=(0.4, 0.2, 0.7, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.42},
            size_hint=(1, None), height=dp(25)))
        self.add_widget(root)

    def on_enter(self):
        Clock.schedule_once(
            lambda dt: setattr(self.manager, 'current', 'lock'), 2.5)


# ══════════════════════════════════════════════════════
#  LOCK SCREEN
# ══════════════════════════════════════════════════════
class LockScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pin_entered = ''
        root = FloatLayout()
        bg(root, C['bg'])

        root.add_widget(lbl(
            ar('شادو مونارك'), size=32, color=C['purple'], bold=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.85},
            size_hint=(1, None), height=dp(52)))
        root.add_widget(lbl(
            ar('أدخل الرمز السري للدخول'), size=13, color=C['sub'],
            pos_hint={'center_x': 0.5, 'center_y': 0.76},
            size_hint=(1, None), height=dp(25)))

        self.pin_display = lbl(
            '○  ○  ○  ○  ○', size=28, color=C['purple'],
            pos_hint={'center_x': 0.5, 'center_y': 0.64},
            size_hint=(1, None), height=dp(42))
        root.add_widget(self.pin_display)

        numpad = BoxLayout(
            orientation='vertical',
            pos_hint={'center_x': 0.5, 'center_y': 0.36},
            size_hint=(0.75, 0.42), spacing=dp(8))
        for row in [['1','2','3'], ['4','5','6'],
                    ['7','8','9'], ['<','0','OK']]:
            rl = BoxLayout(spacing=dp(8))
            for t in row:
                if t == 'OK':
                    col = C['purple2']
                elif t == '<':
                    col = (C['red'][0], C['red'][1], C['red'][2], 0.7)
                else:
                    col = C['card']
                b = styled_btn(t, color=col, font_size=20)
                b.bind(on_press=self.on_btn)
                rl.add_widget(b)
            numpad.add_widget(rl)
        root.add_widget(numpad)

        self.err_lbl = lbl(
            '', size=13, color=C['red'],
            pos_hint={'center_x': 0.5, 'center_y': 0.10},
            size_hint=(1, None), height=dp(28))
        root.add_widget(self.err_lbl)
        self.add_widget(root)

    def on_btn(self, btn):
        t = btn.text
        vibrate_short()
        if t == '<':
            self.pin_entered = self.pin_entered[:-1]
        elif t == 'OK':
            if self.pin_entered == '20057':
                self._update_login()
                self.manager.transition = FadeTransition(duration=0.4)
                self.manager.current = 'main'
            else:
                self.err_lbl.text   = ar('رمز خاطئ! حاول مجدداً')
                self.pin_entered    = ''
                self.pin_display.text = '○  ○  ○  ○  ○'
                Clock.schedule_once(
                    lambda dt: setattr(self.err_lbl, 'text', ''), 2)
            return
        else:
            if len(self.pin_entered) < 5:
                self.pin_entered += t
        f = '●  ' * len(self.pin_entered)
        e = '○  ' * (5 - len(self.pin_entered))
        self.pin_display.text = (f + e).strip()

    def _update_login(self):
        try:
            p     = get_profile()
            today = str(datetime.date.today())
            last  = p.get('last_login', '')
            streak = p.get('streak', 0)
            if last != today:
                yesterday = str(
                    datetime.date.today() - datetime.timedelta(days=1))
                streak = streak + 1 if last == yesterday else 1
                update_profile(last_login=today, streak=streak)
                if streak >= 7:
                    check_achievements()
            if 0 <= datetime.datetime.now().hour < 4:
                con = sqlite3.connect(DB)
                c   = con.cursor()
                c.execute(
                    "UPDATE achievements SET earned=1,date=? "
                    "WHERE name='بومة_الليل' AND earned=0", (today,))
                con.commit()
                con.close()
        except Exception:
            pass


# ══════════════════════════════════════════════════════
#  MAIN SCREEN
# ══════════════════════════════════════════════════════
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        bg(root, C['bg'])

        # Header
        header = BoxLayout(
            pos_hint={'x': 0, 'top': 1},
            size_hint=(1, 0.09), padding=dp(12))
        bg(header, C['header'])
        header.add_widget(lbl(
            ar('شادو مونارك'), size=17, color=C['purple'], bold=True))
        self.clock_lbl = lbl(
            '', size=13, color=C['sub'],
            size_hint=(None, 1), width=dp(80))
        header.add_widget(self.clock_lbl)
        root.add_widget(header)

        # Profile card
        pc = BoxLayout(
            orientation='vertical',
            pos_hint={'center_x': 0.5, 'center_y': 0.76},
            size_hint=(0.93, None), height=dp(105),
            padding=dp(10), spacing=dp(3))
        bg(pc, C['card'], radius=14)
        self.rank_lbl   = lbl(ar('الرتبة: E'),          size=13, color=C['gold'], bold=True)
        self.title_lbl  = lbl(ar('مبتدئ الظل'),          size=12, color=C['sub'])
        self.level_lbl  = lbl(ar('المستوى 1  |  XP: 0'), size=12, color=C['text'])
        self.streak_lbl = lbl(ar('السلسلة: 0 يوم'),      size=11, color=C['green'])
        self.army_lbl   = lbl(ar('جيش الظل: 0'),         size=11, color=C['purple'])
        self.xp_bar     = ProgressBar(max=100, value=0, size_hint=(1, None), height=dp(8))
        for w in [self.rank_lbl, self.title_lbl, self.level_lbl,
                  self.streak_lbl, self.army_lbl, self.xp_bar]:
            pc.add_widget(w)
        root.add_widget(pc)

        # Boss card
        bc = BoxLayout(
            orientation='vertical',
            pos_hint={'center_x': 0.5, 'center_y': 0.59},
            size_hint=(0.93, None), height=dp(58),
            padding=dp(8), spacing=dp(4))
        bg(bc, (0.15, 0.0, 0.05, 0.9), radius=12)
        self.boss_lbl = lbl(ar('الرئيس اليومي: جاري التحميل...'), size=13, color=C['red'], bold=True)
        self.boss_bar = ProgressBar(max=100, value=100, size_hint=(1, None), height=dp(10))
        bc.add_widget(self.boss_lbl)
        bc.add_widget(self.boss_bar)
        root.add_widget(bc)

        # Power bar
        pw = BoxLayout(
            orientation='vertical',
            pos_hint={'center_x': 0.5, 'center_y': 0.48},
            size_hint=(0.93, None), height=dp(42),
            padding=dp(8), spacing=dp(4))
        bg(pw, C['card2'], radius=10)
        self.power_lbl = lbl(ar('القوة: 100%'), size=12, color=C['gold'])
        self.power_bar = ProgressBar(max=100, value=100, size_hint=(1, None), height=dp(8))
        pw.add_widget(self.power_lbl)
        pw.add_widget(self.power_bar)
        root.add_widget(pw)

        # Tools grid
        scroll = ScrollView(pos_hint={'x': 0, 'y': 0.0}, size_hint=(1, 0.40))
        grid = GridLayout(cols=2, size_hint_y=None, padding=dp(8), spacing=dp(7))
        grid.bind(minimum_height=grid.setter('height'))

        tools = [
            ('المهام اليومية',  'tasks',    C['card'],               '⚔'),
            ('الملاحظات',       'notes',    (0.0, 0.08, 0.22, 0.9), '📝'),
            ('مقتطفات الكود',   'snippets', (0.0, 0.12, 0.18, 0.9), '💾'),
            ('الآلة الحاسبة',  'calc',     (0.08, 0.0, 0.2, 0.9),  '🔢'),
            ('بومودورو',         'pomodoro', (0.2, 0.03, 0.05, 0.9), '⏱'),
            ('مولد كلمات السر', 'passgen',  (0.0, 0.15, 0.15, 0.9), '🔑'),
            ('اختبار Regex',    'regex',    (0.05, 0.08, 0.2, 0.9), '🔍'),
            ('منسق JSON',       'jsonf',    (0.0, 0.12, 0.2, 0.9),  '📋'),
            ('محول القواعد',    'baseconv', (0.15, 0.08, 0.0, 0.9), '🔄'),
            ('مولد الهاش',      'hashgen',  (0.0, 0.1, 0.22, 0.9),  '🔐'),
            ('محول الوحدات',    'unitconv', (0.1, 0.15, 0.0, 0.9),  '📐'),
            ('مشفر النصوص',     'b64enc',   (0.15, 0.05, 0.15, 0.9),'🔒'),
            ('الساعة العالمية', 'worldclk', (0.0, 0.05, 0.2, 0.9),  '🌍'),
            ('الإنجازات',       'achieve',  (0.12, 0.08, 0.0, 0.9), '🏆'),
            ('جيش الظل',        'army',     (0.1, 0.0, 0.25, 0.9),  '👥'),
            ('المهارات',        'skills',   (0.05, 0.0, 0.2, 0.9),  '⚡'),
        ]
        for name, screen, color, icon in tools:
            btn = styled_btn(
                f'{icon}\n{ar(name)}',
                color=color, font_size=12,
                size_hint_y=None, height=dp(62))
            btn.bind(on_press=lambda x, s=screen: self.go_to(s))
            grid.add_widget(btn)

        scroll.add_widget(grid)
        root.add_widget(scroll)
        self.add_widget(root)

        Clock.schedule_interval(self.update_clock, 1)
        Clock.schedule_once(self.refresh_profile, 0.5)
        Clock.schedule_interval(self.refresh_profile, 30)

    def go_to(self, screen):
        vibrate_short()
        self.manager.transition = SlideTransition(direction='left', duration=0.25)
        self.manager.current = screen

    def update_clock(self, dt):
        try:
            self.clock_lbl.text = datetime.datetime.now().strftime('%H:%M:%S')
        except Exception:
            pass

    def refresh_profile(self, dt=None):
        try:
            p = get_profile()
            self.rank_lbl.text   = ar(f'الرتبة: {p["rank"]}')
            self.rank_lbl.color  = RANK_COLORS.get(p['rank'], C['gold'])
            self.title_lbl.text  = ar(p['title'])
            xp_need = p['level'] * 100
            self.level_lbl.text  = ar(f'المستوى {p["level"]}  |  XP: {p["xp"]}/{xp_need}')
            self.xp_bar.max      = xp_need
            self.xp_bar.value    = p['xp']
            self.streak_lbl.text = ar(f'السلسلة: {p["streak"]} يوم')
            self.army_lbl.text   = ar(f'جيش الظل: {p["army"]}')
            self.power_lbl.text  = ar(f'القوة: {p["power"]}%')
            self.power_bar.value = p['power']

            con   = sqlite3.connect(DB)
            c     = con.cursor()
            today = str(datetime.date.today())
            c.execute('SELECT * FROM boss WHERE id=1')
            boss = c.fetchone()
            if boss:
                if boss[4] != today:
                    bosses = ['وحش الظل', 'الشبح الداكن', 'سالك الفراغ',
                              'رعب الليل', 'رب الهاوية']
                    c.execute(
                        'UPDATE boss SET name=?,hp=100,max_hp=100,date=? WHERE id=1',
                        (random.choice(bosses), today))
                    con.commit()
                    c.execute('SELECT * FROM boss WHERE id=1')
                    boss = c.fetchone()
                self.boss_lbl.text  = ar(f'الرئيس: {boss[1]}  ❤ {boss[2]}/{boss[3]}')
                self.boss_bar.max   = boss[3]
                self.boss_bar.value = boss[2]
            con.close()
        except Exception:
            pass

    def on_enter(self):
        self.refresh_profile()


# ══════════════════════════════════════════════════════
#  TASKS SCREEN
# ══════════════════════════════════════════════════════
class TasksScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header(
            ar('المهام اليومية ⚔'),
            back_cb=lambda x: go_back(self.manager)))

        self.scroll = ScrollView(pos_hint={'x': 0, 'y': 0.15}, size_hint=(1, 0.78))
        self.tl = BoxLayout(orientation='vertical', size_hint_y=None,
                            spacing=dp(7), padding=dp(9))
        self.tl.bind(minimum_height=self.tl.setter('height'))
        self.scroll.add_widget(self.tl)
        root.add_widget(self.scroll)

        inp = BoxLayout(pos_hint={'x': 0, 'y': 0}, size_hint=(1, 0.14),
                        padding=dp(8), spacing=dp(8))
        self.task_inp = TextInput(
            hint_text=ar('مهمة جديدة...'),
            background_color=C['card2'][:3] + (1,),
            foreground_color=C['text'],
            font_name=DEFAULT_FONT, font_size=dp(14), multiline=False)
        add_btn = styled_btn('+', color=C['purple2'], size_hint=(None, 1), width=dp(52))
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
            c   = con.cursor()
            c.execute('SELECT * FROM tasks ORDER BY done ASC, id DESC')
            tasks = c.fetchall()
            con.close()
            for t in tasks:
                done = t[2]
                row  = BoxLayout(size_hint_y=None, height=dp(55),
                                 spacing=dp(7), padding=dp(8))
                bg(row, (0.04, 0.18, 0.04, 0.9) if done else C['card'], radius=8)
                l = lbl(ar(t[1]), size=13,
                        color=C['green'] if done else C['text'],
                        halign='right',
                        text_size=(Window.width * 0.52, None))
                xp_l = lbl(f'+{t[4]}XP', size=10, color=C['gold'],
                            size_hint=(None, 1), width=dp(42))
                db = styled_btn(
                    '✓' if not done else '↩',
                    color=C['green'] if not done else (0.3, 0.3, 0.3, 1),
                    size_hint=(None, 1), width=dp(40))
                db.bind(on_press=lambda x, tid=t[0], d=done: self.toggle(tid, d))
                xb = styled_btn('✕', color=C['red'][:3] + (0.8,),
                                size_hint=(None, 1), width=dp(36))
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
                c   = con.cursor()
                xp  = random.randint(10, 30)
                c.execute(
                    'INSERT INTO tasks (text,done,date,xp_reward,priority) VALUES (?,0,?,?,?)',
                    (text, str(datetime.date.today()), xp, 1))
                con.commit()
                con.close()
                self.task_inp.text = ''
                self.refresh()
            except Exception:
                pass

    def toggle(self, tid, done):
        try:
            con      = sqlite3.connect(DB)
            c        = con.cursor()
            new_done = 0 if done else 1
            c.execute('UPDATE tasks SET done=? WHERE id=?', (new_done, tid))
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
                        today = str(datetime.date.today())
                        c.execute(
                            "UPDATE achievements SET earned=1,date=? "
                            "WHERE name='قاتل_الرئيس' AND earned=0", (today,))
                    send_notification(ar('مهمة مكتملة!'), ar(f'+{row[0]} XP'))
                    vibrate_short()
            con.commit()
            con.close()
            self.refresh()
            try:
                self.manager.get_screen('main').refresh_profile()
            except Exception:
                pass
        except Exception:
            pass

    def delete(self, tid):
        try:
            con = sqlite3.connect(DB)
            c   = con.cursor()
            c.execute('DELETE FROM tasks WHERE id=?', (tid,))
            con.commit()
            con.close()
            self.refresh()
        except Exception:
            pass


# ══════════════════════════════════════════════════════
#  NOTES SCREEN
# ══════════════════════════════════════════════════════
class NotesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header(
            ar('الملاحظات 📝'),
            back_cb=lambda x: go_back(self.manager)))

        self.scroll = ScrollView(pos_hint={'x': 0, 'y': 0.18}, size_hint=(1, 0.74))
        self.nl = BoxLayout(orientation='vertical', size_hint_y=None,
                            spacing=dp(8), padding=dp(10))
        self.nl.bind(minimum_height=self.nl.setter('height'))
        self.scroll.add_widget(self.nl)
        root.add_widget(self.scroll)

        inp = BoxLayout(pos_hint={'x': 0, 'y': 0}, size_hint=(1, 0.17),
                        padding=dp(8), spacing=dp(8))
        self.note_inp = TextInput(
            hint_text=ar('اكتب ملاحظة...'),
            background_color=C['card2'][:3] + (1,),
            foreground_color=C['text'],
            font_name=DEFAULT_FONT, font_size=dp(14))
        add_btn = styled_btn('+', color=C['purple2'], size_hint=(None, 1), width=dp(52))
        add_btn.bind(on_press=self.add_note)
        inp.add_widget(self.note_inp)
        inp.add_widget(add_btn)
        root.add_widget(inp)
        self.add_widget(root)
        self.refresh()

    def refresh(self):
        self.nl.clear_widgets()
        try:
            con   = sqlite3.connect(DB)
            c     = con.cursor()
            c.execute('SELECT * FROM notes ORDER BY id DESC')
            notes = c.fetchall()
            con.close()
            for n in notes:
                row = BoxLayout(size_hint_y=None, height=dp(62),
                                spacing=dp(8), padding=dp(6))
                bg(row, C['card'], radius=8)
                preview = n[1][:55] + ('...' if len(n[1]) > 55 else '')
                l = lbl(ar(preview), size=13, halign='right',
                        text_size=(Window.width * 0.65, None))
                t_l = lbl(n[2][-5:] if n[2] else '', size=9,
                           color=C['sub'], size_hint=(None, 1), width=dp(38))
                xb = styled_btn('✕', color=C['red'][:3] + (0.8,),
                                size_hint=(None, 1), width=dp(38))
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
                c   = con.cursor()
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
            c   = con.cursor()
            c.execute('DELETE FROM notes WHERE id=?', (nid,))
            con.commit()
            con.close()
            self.refresh()
        except Exception:
            pass


# ══════════════════════════════════════════════════════
#  SNIPPETS SCREEN
# ══════════════════════════════════════════════════════
class SnippetsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header(
            ar('مقتطفات الكود 💾'),
            back_cb=lambda x: go_back(self.manager)))

        self.scroll = ScrollView(pos_hint={'x': 0, 'y': 0.25}, size_hint=(1, 0.68))
        self.sl = BoxLayout(orientation='vertical', size_hint_y=None,
                            spacing=dp(8), padding=dp(10))
        self.sl.bind(minimum_height=self.sl.setter('height'))
        self.scroll.add_widget(self.sl)
        root.add_widget(self.scroll)

        inp = BoxLayout(orientation='vertical', pos_hint={'x': 0, 'y': 0},
                        size_hint=(1, 0.24), padding=dp(8), spacing=dp(6))
        self.t_inp = TextInput(
            hint_text=ar('العنوان...'), multiline=False,
            background_color=C['card2'][:3] + (1,), foreground_color=C['text'],
            font_name=DEFAULT_FONT, size_hint_y=None, height=dp(38), font_size=dp(13))
        self.c_inp = TextInput(
            hint_text=ar('الكود هنا...'),
            background_color=(0.03, 0.0, 0.1, 1), foreground_color=(0.4, 1, 0.4, 1),
            font_name=DEFAULT_FONT, font_size=dp(12))
        sb = styled_btn(ar('حفظ المقتطف'), color=C['purple2'],
                        size_hint_y=None, height=dp(35))
        sb.bind(on_press=self.add_snip)
        for w in [self.t_inp, self.c_inp, sb]:
            inp.add_widget(w)
        root.add_widget(inp)
        self.add_widget(root)
        self.refresh()

    def refresh(self):
        self.sl.clear_widgets()
        try:
            con   = sqlite3.connect(DB)
            c     = con.cursor()
            c.execute('SELECT * FROM snippets ORDER BY id DESC')
            snips = c.fetchall()
            con.close()
            for s in snips:
                card = BoxLayout(size_hint_y=None, height=dp(70),
                                 spacing=dp(8), padding=dp(8))
                bg(card, C['card2'], radius=8)
                info = BoxLayout(orientation='vertical')
                info.add_widget(lbl(ar(s[1]), size=13, bold=True,
                                    color=C['purple'], halign='right'))
                preview = s[2][:40] + '...' if len(s[2]) > 40 else s[2]
                info.add_widget(lbl(preview, size=11,
                                    color=(0.4, 1, 0.4, 1), halign='left'))
                cb = styled_btn(ar('نسخ'), color=(0, 0.35, 0.15, 1),
                                size_hint=(None, 1), width=dp(55))
                cb.bind(on_press=lambda x, code=s[2]: Clipboard.copy(code))
                xb = styled_btn('✕', color=C['red'][:3] + (0.8,),
                                size_hint=(None, 1), width=dp(36))
                xb.bind(on_press=lambda x, sid=s[0]: self.delete(sid))
                card.add_widget(info)
                card.add_widget(cb)
                card.add_widget(xb)
                self.sl.add_widget(card)
        except Exception:
            pass

    def add_snip(self, *a):
        t      = self.t_inp.text.strip()
        c_text = self.c_inp.text.strip()
        if t and c_text:
            try:
                con = sqlite3.connect(DB)
                cur = con.cursor()
                cur.execute('INSERT INTO snippets (title,code) VALUES (?,?)', (t, c_text))
                con.commit()
                cur.execute('SELECT COUNT(*) FROM snippets')
                cnt = cur.fetchone()[0]
                if cnt >= 10:
                    today = str(datetime.date.today())
                    cur.execute(
                        "UPDATE achievements SET earned=1,date=? "
                        "WHERE name='حارس_الكود' AND earned=0", (today,))
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
            c   = con.cursor()
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
        root.add_widget(make_header(
            ar('الآلة الحاسبة 🔢'),
            back_cb=lambda x: go_back(self.manager)))

        self.disp = lbl('0', size=34, color=C['text'], bold=True,
                        pos_hint={'center_x': 0.5, 'center_y': 0.80},
                        size_hint=(0.92, None), height=dp(55), halign='right')
        self.sub_disp = lbl('', size=12, color=C['sub'],
                            pos_hint={'center_x': 0.5, 'center_y': 0.71},
                            size_hint=(0.92, None), height=dp(22), halign='right')
        root.add_widget(self.disp)
        root.add_widget(self.sub_disp)

        grid = GridLayout(cols=4,
                          pos_hint={'center_x': 0.5, 'center_y': 0.37},
                          size_hint=(0.95, 0.54), spacing=dp(6))
        btns = [
            ('C',   (0.4, 0.0, 0.1, 1)),  ('()',  (0.2, 0.0, 0.4, 1)),
            ('%',   (0.2, 0.0, 0.4, 1)),  ('/',   (0.35, 0.0, 0.7, 1)),
            ('7',   None),                  ('8',   None),
            ('9',   None),                  ('×',   (0.35, 0.0, 0.7, 1)),
            ('4',   None),                  ('5',   None),
            ('6',   None),                  ('−',   (0.35, 0.0, 0.7, 1)),
            ('1',   None),                  ('2',   None),
            ('3',   None),                  ('+',   (0.35, 0.0, 0.7, 1)),
            ('HEX', (0, 0.2, 0.4, 1)),     ('0',   None),
            ('.',   None),                  ('=',   (0.5, 0.0, 0.9, 1)),
        ]
        for t, col in btns:
            b = styled_btn(t, color=col if col else C['card'], font_size=18)
            b.bind(on_press=self.on_calc)
            grid.add_widget(b)
        root.add_widget(grid)
        self.add_widget(root)

    def on_calc(self, btn):
        t = btn.text
        vibrate_short()
        if t == 'C':
            self.expr         = ''
            self.disp.text    = '0'
            self.sub_disp.text = ''
        elif t == '=':
            try:
                expr = self.expr.replace('×', '*').replace('−', '-')
                r    = eval(expr)
                self.sub_disp.text = self.expr
                self.disp.text     = str(r)
                self.expr          = str(r)
            except Exception:
                self.disp.text = ar('خطأ')
                self.expr      = ''
        elif t == 'HEX':
            try:
                v = int(eval(self.expr.replace('×', '*').replace('−', '-')))
                self.sub_disp.text = (f'HEX: {hex(v)[2:].upper()}  '
                                      f'BIN: {bin(v)[2:]}  '
                                      f'OCT: {oct(v)[2:]}')
            except Exception:
                self.sub_disp.text = ar('ليس عدداً صحيحاً')
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
        self.seconds_left = 25 * 60
        self.running      = False
        self.is_break     = False
        self.sessions     = 0
        self._clock       = None
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header(
            ar('مؤقت بومودورو ⏱'),
            back_cb=lambda x: go_back(self.manager)))

        self.mode_lbl = lbl(ar('تركيز'), size=20, color=C['red'], bold=True,
                            pos_hint={'center_x': 0.5, 'center_y': 0.80},
                            size_hint=(1, None), height=dp(32))
        self.timer_lbl = lbl('25:00', size=66, color=C['text'], bold=True,
                             pos_hint={'center_x': 0.5, 'center_y': 0.65},
                             size_hint=(1, None), height=dp(85))
        self.sess_lbl = lbl(ar('الجلسات: 0'), size=14, color=C['sub'],
                            pos_hint={'center_x': 0.5, 'center_y': 0.54},
                            size_hint=(1, None), height=dp(28))

        btns = BoxLayout(pos_hint={'center_x': 0.5, 'center_y': 0.43},
                         size_hint=(0.8, None), height=dp(55), spacing=dp(12))
        self.start_btn = styled_btn(ar('ابدأ'), color=C['green'][:3] + (1,), font_size=19)
        self.start_btn.bind(on_press=self.toggle)
        reset_btn = styled_btn(ar('إعادة'), color=C['red'][:3] + (0.8,), font_size=19)
        reset_btn.bind(on_press=self.reset)
        btns.add_widget(self.start_btn)
        btns.add_widget(reset_btn)

        for w in [self.mode_lbl, self.timer_lbl, self.sess_lbl, btns]:
            root.add_widget(w)
        self.add_widget(root)

    def toggle(self, *a):
        if self.running:
            self.running = False
            if self._clock:
                self._clock.cancel()
            self.start_btn.text = ar('ابدأ')
        else:
            self.running    = True
            self._clock     = Clock.schedule_interval(self.tick, 1)
            self.start_btn.text = ar('إيقاف')

    def tick(self, dt):
        if self.seconds_left > 0:
            self.seconds_left -= 1
            m, s = divmod(self.seconds_left, 60)
            self.timer_lbl.text = f'{m:02d}:{s:02d}'
        else:
            if not self.is_break:
                self.sessions += 1
                self.sess_lbl.text  = ar(f'الجلسات: {self.sessions}')
                add_xp(25)
                send_notification(ar('انتهى وقت التركيز!'), ar('خذ 5 دقائق راحة'))
                self.is_break       = True
                self.seconds_left   = 5 * 60
                self.mode_lbl.text  = ar('استراحة')
                self.mode_lbl.color = C['green']
            else:
                self.is_break       = False
                self.seconds_left   = 25 * 60
                self.mode_lbl.text  = ar('تركيز')
                self.mode_lbl.color = C['red']

    def reset(self, *a):
        self.running = False
        if self._clock:
            self._clock.cancel()
        self.is_break          = False
        self.seconds_left      = 25 * 60
        self.timer_lbl.text    = '25:00'
        self.mode_lbl.text     = ar('تركيز')
        self.mode_lbl.color    = C['red']
        self.start_btn.text    = ar('ابدأ')


# ══════════════════════════════════════════════════════
#  PASSWORD GENERATOR
# ══════════════════════════════════════════════════════
class PassGenScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inc_upper   = True
        self.inc_digits  = True
        self.inc_symbols = True
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header(
            ar('مولد كلمات السر 🔑'),
            back_cb=lambda x: go_back(self.manager)))

        self.result_lbl = lbl(
            ar('اضغط توليد'), size=15, color=(0.5, 1, 0.5, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.73},
            size_hint=(0.9, None), height=dp(48), halign='center')
        root.add_widget(self.result_lbl)

        self.len_lbl = lbl(ar('الطول: 16'), size=14, color=C['text'],
                           pos_hint={'center_x': 0.5, 'center_y': 0.62},
                           size_hint=(1, None), height=dp(25))
        self.slider = Slider(min=8, max=32, value=16, step=1,
                             pos_hint={'center_x': 0.5, 'center_y': 0.54},
                             size_hint=(0.85, None), height=dp(40))
        self.slider.bind(value=lambda s, v: setattr(
            self.len_lbl, 'text', ar(f'الطول: {int(v)}')))

        opts = BoxLayout(pos_hint={'center_x': 0.5, 'center_y': 0.43},
                         size_hint=(0.85, None), height=dp(44), spacing=dp(8))
        self.bu = styled_btn('ABC', color=C['purple2'], font_size=14)
        self.bd = styled_btn('123', color=C['purple2'], font_size=14)
        self.bs = styled_btn('#@!', color=C['purple2'], font_size=14)
        self.bu.bind(on_press=lambda x: self.tog('u'))
        self.bd.bind(on_press=lambda x: self.tog('d'))
        self.bs.bind(on_press=lambda x: self.tog('s'))
        for b in [self.bu, self.bd, self.bs]:
            opts.add_widget(b)

        gen_btn = styled_btn(ar('توليد'), color=C['purple2'], font_size=19,
                             size_hint=(0.6, None), height=dp(54),
                             pos_hint={'center_x': 0.5, 'center_y': 0.29})
        gen_btn.bind(on_press=self.generate)
        copy_btn = styled_btn(ar('نسخ'), color=(0, 0.35, 0.15, 1), font_size=14,
                              size_hint=(0.5, None), height=dp(40),
                              pos_hint={'center_x': 0.5, 'center_y': 0.18})
        copy_btn.bind(on_press=lambda x: Clipboard.copy(self.result_lbl.text))

        for w in [self.result_lbl, self.len_lbl, self.slider, opts, gen_btn, copy_btn]:
            root.add_widget(w)
        self.add_widget(root)

    def tog(self, opt):
        if opt == 'u':
            self.inc_upper = not self.inc_upper
            self.bu.color  = C['green'] if self.inc_upper else C['sub']
        elif opt == 'd':
            self.inc_digits = not self.inc_digits
            self.bd.color   = C['green'] if self.inc_digits else C['sub']
        elif opt == 's':
            self.inc_symbols = not self.inc_symbols
            self.bs.color    = C['green'] if self.inc_symbols else C['sub']

    def generate(self, *a):
        chars = string.ascii_lowercase
        if self.inc_upper:   chars += string.ascii_uppercase
        if self.inc_digits:  chars += string.digits
        if self.inc_symbols: chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
        length = int(self.slider.value)
        self.result_lbl.text = ''.join(random.choice(chars) for _ in range(length))


# ══════════════════════════════════════════════════════
#  REGEX TESTER
# ══════════════════════════════════════════════════════
class RegexScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header(
            ar('اختبار Regex 🔍'),
            back_cb=lambda x: go_back(self.manager)))

        content = BoxLayout(orientation='vertical',
                            pos_hint={'x': 0, 'y': 0}, size_hint=(1, 0.93),
                            padding=dp(10), spacing=dp(8))
        content.add_widget(lbl(ar('النمط (Pattern):'), size=13, color=C['purple'],
                               size_hint_y=None, height=dp(22), halign='right'))
        self.pat = TextInput(hint_text=r'\d+', multiline=False,
                             background_color=C['card2'][:3] + (1,),
                             foreground_color=(1, 1, 0, 1),
                             font_name=DEFAULT_FONT, font_size=dp(14),
                             size_hint_y=None, height=dp(42))
        content.add_widget(self.pat)
        content.add_widget(lbl(ar('النص للاختبار:'), size=13, color=C['purple'],
                               size_hint_y=None, height=dp(22), halign='right'))
        self.test_inp = TextInput(hint_text=ar('أدخل النص هنا...'),
                                  background_color=C['card2'][:3] + (1,),
                                  foreground_color=C['text'],
                                  font_name=DEFAULT_FONT, font_size=dp(13),
                                  size_hint_y=None, height=dp(80))
        content.add_widget(self.test_inp)
        tb = styled_btn(ar('اختبار'), color=C['purple2'], font_size=17,
                        size_hint_y=None, height=dp(46))
        tb.bind(on_press=self.test_regex)
        content.add_widget(tb)
        self.res = lbl('', size=13, color=C['green'], halign='left',
                       text_size=(Window.width - dp(20), None))
        content.add_widget(self.res)
        root.add_widget(content)
        self.add_widget(root)

    def test_regex(self, *a):
        try:
            m = re.findall(self.pat.text, self.test_inp.text)
            if m:
                self.res.color = C['green']
                self.res.text  = (ar(f'وجدت {len(m)} تطابق:') + '\n'
                                  + '\n'.join(str(x) for x in m[:12]))
            else:
                self.res.color = C['red']
                self.res.text  = ar('لا يوجد تطابق')
        except Exception as e:
            self.res.color = C['gold']
            self.res.text  = f'Error: {e}'


# ══════════════════════════════════════════════════════
#  JSON FORMATTER
# ══════════════════════════════════════════════════════
class JsonScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header(
            ar('منسق JSON 📋'),
            back_cb=lambda x: go_back(self.manager)))

        content = BoxLayout(orientation='vertical',
                            pos_hint={'x': 0, 'y': 0}, size_hint=(1, 0.93),
                            padding=dp(10), spacing=dp(8))
        self.inp = TextInput(hint_text=ar('الصق JSON هنا...'),
                             background_color=(0.03, 0.0, 0.1, 1),
                             foreground_color=C['text'],
                             font_name=DEFAULT_FONT, font_size=dp(12))
        btns = BoxLayout(size_hint_y=None, height=dp(46), spacing=dp(8))
        for btn_txt, cb, col in [
            (ar('تنسيق'),  self.fmt, C['purple2']),
            (ar('تحقق'),   self.val, (0, 0.3, 0.15, 1)),
            (ar('نسخ'),    lambda x: Clipboard.copy(self.inp.text), (0.2, 0.1, 0, 1)),
        ]:
            b = styled_btn(btn_txt, color=col, font_size=15)
            b.bind(on_press=cb)
            btns.add_widget(b)
        self.status = lbl('', size=13, color=C['green'],
                          size_hint_y=None, height=dp(28))
        content.add_widget(self.inp)
        content.add_widget(btns)
        content.add_widget(self.status)
        root.add_widget(content)
        self.add_widget(root)

    def fmt(self, *a):
        try:
            self.inp.text     = json.dumps(json.loads(self.inp.text),
                                           indent=2, ensure_ascii=False)
            self.status.color = C['green']
            self.status.text  = ar('تم التنسيق بنجاح ✓')
        except Exception as e:
            self.status.color = C['red']
            self.status.text  = f'Error: {e}'

    def val(self, *a):
        try:
            json.loads(self.inp.text)
            self.status.color = C['green']
            self.status.text  = ar('JSON صحيح ✓')
        except Exception as e:
            self.status.color = C['red']
            self.status.text  = f'Error: {e}'


# ══════════════════════════════════════════════════════
#  BASE CONVERTER
# ══════════════════════════════════════════════════════
class BaseConvScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header(
            ar('محول القواعد 🔄'),
            back_cb=lambda x: go_back(self.manager)))

        content = BoxLayout(orientation='vertical',
                            pos_hint={'x': 0, 'y': 0}, size_hint=(1, 0.93),
                            padding=dp(15), spacing=dp(10))
        self.fields = {}
        for label_txt, key, color in [
            (ar('عشري  (Decimal)'),   'dec', C['text']),
            (ar('ستة عشري (Hex)'),   'hex', (1, 0.8, 0, 1)),
            (ar('ثنائي  (Binary)'),  'bin', (0.4, 1, 0.4, 1)),
            (ar('ثماني  (Octal)'),   'oct', (0.6, 0.8, 1, 1)),
        ]:
            content.add_widget(lbl(label_txt, size=13, color=C['purple'],
                                   size_hint_y=None, height=dp(20), halign='right'))
            inp = TextInput(multiline=False,
                            background_color=C['card2'][:3] + (1,),
                            foreground_color=color, font_name=DEFAULT_FONT,
                            font_size=dp(14), size_hint_y=None, height=dp(42))
            self.fields[key] = inp
            content.add_widget(inp)
        cb = styled_btn(ar('تحويل'), color=C['purple2'], font_size=17,
                        size_hint_y=None, height=dp(50))
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
            else:               return
            f['dec'].text = str(val)
            f['hex'].text = hex(val)[2:].upper()
            f['bin'].text = bin(val)[2:]
            f['oct'].text = oct(val)[2:]
        except Exception:
            for fld in self.fields.values():
                fld.text = ar('خطأ')


# ══════════════════════════════════════════════════════
#  HASH GENERATOR  ★ جديد
# ══════════════════════════════════════════════════════
class HashGenScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header(
            ar('مولد الهاش 🔐'),
            back_cb=lambda x: go_back(self.manager)))

        content = BoxLayout(orientation='vertical',
                            pos_hint={'x': 0, 'y': 0}, size_hint=(1, 0.93),
                            padding=dp(12), spacing=dp(8))
        content.add_widget(lbl(ar('أدخل النص:'), size=13, color=C['purple'],
                               size_hint_y=None, height=dp(22), halign='right'))
        self.inp = TextInput(
            hint_text=ar('النص هنا...'),
            background_color=C['card2'][:3] + (1,), foreground_color=C['text'],
            font_name=DEFAULT_FONT, font_size=dp(13),
            size_hint_y=None, height=dp(70))
        content.add_widget(self.inp)

        gen_btn = styled_btn(ar('توليد الهاش'), color=C['purple2'], font_size=16,
                             size_hint_y=None, height=dp(48))
        gen_btn.bind(on_press=self.generate)
        content.add_widget(gen_btn)

        scroll = ScrollView()
        self.result_box = BoxLayout(orientation='vertical', size_hint_y=None,
                                    spacing=dp(6), padding=dp(4))
        self.result_box.bind(minimum_height=self.result_box.setter('height'))
        scroll.add_widget(self.result_box)
        content.add_widget(scroll)
        root.add_widget(content)
        self.add_widget(root)

    def generate(self, *a):
        text = self.inp.text
        if not text:
            return
        self.result_box.clear_widgets()
        encoded = text.encode('utf-8')
        algos = [
            ('MD5',     hashlib.md5(encoded).hexdigest()),
            ('SHA-1',   hashlib.sha1(encoded).hexdigest()),
            ('SHA-256', hashlib.sha256(encoded).hexdigest()),
            ('SHA-512', hashlib.sha512(encoded).hexdigest()),
        ]
        for name, h_val in algos:
            card = BoxLayout(size_hint_y=None, height=dp(75),
                             spacing=dp(8), padding=dp(8))
            bg(card, C['card2'], radius=8)
            info = BoxLayout(orientation='vertical')
            info.add_widget(lbl(name, size=13, bold=True, color=C['cyan'], halign='left'))
            info.add_widget(lbl(h_val[:38] + '...', size=10,
                                color=C['text'], halign='left'))
            info.add_widget(lbl(h_val[38:], size=10, color=C['sub'], halign='left'))
            cb = styled_btn(ar('نسخ'), color=(0, 0.35, 0.15, 1),
                            size_hint=(None, 1), width=dp(55))
            cb.bind(on_press=lambda x, v=h_val: Clipboard.copy(v))
            card.add_widget(info)
            card.add_widget(cb)
            self.result_box.add_widget(card)


# ══════════════════════════════════════════════════════
#  UNIT CONVERTER  ★ جديد
# ══════════════════════════════════════════════════════
class UnitConvScreen(Screen):

    CATEGORIES = ['الطول', 'الوزن', 'درجة الحرارة', 'المساحة', 'السرعة']

    UNITS = {
        'الطول': {
            'متر':      1.0,
            'كيلومتر':  1000.0,
            'سنتيمتر':  0.01,
            'مليمتر':   0.001,
            'ميل':      1609.34,
            'قدم':      0.3048,
            'بوصة':     0.0254,
        },
        'الوزن': {
            'كيلوغرام': 1.0,
            'غرام':     0.001,
            'مليغرام':  0.000001,
            'طن':       1000.0,
            'باوند':    0.453592,
            'أونصة':    0.0283495,
        },
        'درجة الحرارة': {
            'مئوي °C':     'C',
            'فهرنهايت °F': 'F',
            'كلفن K':      'K',
        },
        'المساحة': {
            'متر مربع':      1.0,
            'كم مربع':       1_000_000.0,
            'هكتار':         10_000.0,
            'قدم مربع':      0.092903,
            'ميل مربع':      2_589_988.0,
        },
        'السرعة': {
            'م/ث':   1.0,
            'كم/س':  0.277778,
            'ميل/س': 0.44704,
            'عقدة':  0.514444,
        },
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cur_cat   = self.CATEGORIES[0]
        self.from_unit = None
        self.to_unit   = None
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header(
            ar('محول الوحدات 📐'),
            back_cb=lambda x: go_back(self.manager)))

        content = BoxLayout(orientation='vertical',
                            pos_hint={'x': 0, 'y': 0}, size_hint=(1, 0.93),
                            padding=dp(12), spacing=dp(7))

        # Category row
        cat_scroll = ScrollView(size_hint_y=None, height=dp(46))
        cat_box    = BoxLayout(size_hint_x=None, spacing=dp(5), padding=(dp(4), 0))
        cat_box.bind(minimum_width=cat_box.setter('width'))
        for cat in self.CATEGORIES:
            b = styled_btn(ar(cat), color=C['card'], font_size=12,
                           size_hint=(None, 1), width=dp(110))
            b.bind(on_press=lambda x, c=cat: self.set_cat(c))
            cat_box.add_widget(b)
        cat_scroll.add_widget(cat_box)
        content.add_widget(cat_scroll)

        content.add_widget(lbl(ar('القيمة:'), size=13, color=C['purple'],
                               size_hint_y=None, height=dp(20), halign='right'))
        self.val_inp = TextInput(
            hint_text='0.0', multiline=False,
            background_color=C['card2'][:3] + (1,), foreground_color=C['text'],
            font_name=DEFAULT_FONT, font_size=dp(15),
            size_hint_y=None, height=dp(46))
        content.add_widget(self.val_inp)

        content.add_widget(lbl(ar('من:'), size=13, color=C['purple'],
                               size_hint_y=None, height=dp(20), halign='right'))
        self.from_scroll = ScrollView(size_hint_y=None, height=dp(46))
        self.from_box    = BoxLayout(size_hint_x=None, spacing=dp(5), padding=(dp(4), 0))
        self.from_box.bind(minimum_width=self.from_box.setter('width'))
        self.from_scroll.add_widget(self.from_box)
        content.add_widget(self.from_scroll)

        content.add_widget(lbl(ar('إلى:'), size=13, color=C['purple'],
                               size_hint_y=None, height=dp(20), halign='right'))
        self.to_scroll = ScrollView(size_hint_y=None, height=dp(46))
        self.to_box    = BoxLayout(size_hint_x=None, spacing=dp(5), padding=(dp(4), 0))
        self.to_box.bind(minimum_width=self.to_box.setter('width'))
        self.to_scroll.add_widget(self.to_box)
        content.add_widget(self.to_scroll)

        conv_btn = styled_btn(ar('تحويل'), color=C['purple2'], font_size=17,
                              size_hint_y=None, height=dp(50))
        conv_btn.bind(on_press=self.convert)
        content.add_widget(conv_btn)

        self.result_lbl = lbl('', size=24, color=C['gold'], bold=True,
                              size_hint_y=None, height=dp(52))
        content.add_widget(self.result_lbl)

        root.add_widget(content)
        self.add_widget(root)
        self.set_cat(self.cur_cat)

    def set_cat(self, cat):
        self.cur_cat   = cat
        self.from_unit = None
        self.to_unit   = None
        self._build_btns(self.from_box, 'from')
        self._build_btns(self.to_box,   'to')

    def _build_btns(self, box, which):
        box.clear_widgets()
        for u in self.UNITS.get(self.cur_cat, {}).keys():
            b = styled_btn(ar(u), color=C['card2'], font_size=11,
                           size_hint=(None, 1), width=dp(100))
            b.bind(on_press=lambda x, uu=u, w=which: self.select_unit(uu, w))
            box.add_widget(b)

    def select_unit(self, unit, which):
        if which == 'from':
            self.from_unit = unit
        else:
            self.to_unit = unit

    def convert(self, *a):
        try:
            val = float(self.val_inp.text)
            if not self.from_unit or not self.to_unit:
                self.result_lbl.text = ar('اختر وحدتي التحويل')
                return
            units = self.UNITS.get(self.cur_cat, {})
            if self.cur_cat == 'درجة الحرارة':
                f = units.get(self.from_unit)
                t = units.get(self.to_unit)
                base = (val if f == 'C' else
                        (val - 32) * 5 / 9 if f == 'F' else val - 273.15)
                r = (base if t == 'C' else
                     base * 9 / 5 + 32 if t == 'F' else base + 273.15)
            else:
                base = val * units.get(self.from_unit, 1)
                r    = base / units.get(self.to_unit, 1)
            self.result_lbl.text = ar(f'النتيجة: {r:.6g}')
        except Exception:
            self.result_lbl.text = ar('خطأ في الإدخال')


# ══════════════════════════════════════════════════════
#  BASE64 / URL ENCODER  ★ جديد
# ══════════════════════════════════════════════════════
class Base64Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header(
            ar('مشفر النصوص 🔒'),
            back_cb=lambda x: go_back(self.manager)))

        content = BoxLayout(orientation='vertical',
                            pos_hint={'x': 0, 'y': 0}, size_hint=(1, 0.93),
                            padding=dp(12), spacing=dp(8))
        content.add_widget(lbl(ar('النص المدخل:'), size=13, color=C['purple'],
                               size_hint_y=None, height=dp(22), halign='right'))
        self.inp = TextInput(
            hint_text=ar('أدخل النص هنا...'),
            background_color=C['card2'][:3] + (1,), foreground_color=C['text'],
            font_name=DEFAULT_FONT, font_size=dp(13),
            size_hint_y=None, height=dp(90))
        content.add_widget(self.inp)

        btns = BoxLayout(size_hint_y=None, height=dp(46), spacing=dp(6))
        for btn_txt, cb, col in [
            (ar('تشفير B64'),  self.encode_b64,  C['purple2']),
            (ar('فك B64'),     self.decode_b64,  (0, 0.3, 0.15, 1)),
            (ar('URL تشفير'),  self.url_encode,   (0.2, 0.1, 0, 1)),
            (ar('URL فك'),     self.url_decode,   (0.1, 0.15, 0.05, 1)),
        ]:
            b = styled_btn(btn_txt, color=col, font_size=12)
            b.bind(on_press=cb)
            btns.add_widget(b)
        content.add_widget(btns)

        content.add_widget(lbl(ar('النتيجة:'), size=13, color=C['purple'],
                               size_hint_y=None, height=dp(22), halign='right'))
        self.out = TextInput(
            hint_text=ar('النتيجة ستظهر هنا...'),
            background_color=(0.03, 0.0, 0.1, 1), foreground_color=(0.4, 1, 0.4, 1),
            font_name=DEFAULT_FONT, font_size=dp(13),
            size_hint_y=None, height=dp(120))
        content.add_widget(self.out)

        copy_btn = styled_btn(ar('نسخ النتيجة'), color=(0, 0.35, 0.15, 1), font_size=14,
                              size_hint_y=None, height=dp(44))
        copy_btn.bind(on_press=lambda x: Clipboard.copy(self.out.text))
        content.add_widget(copy_btn)
        root.add_widget(content)
        self.add_widget(root)

    def encode_b64(self, *a):
        try:
            self.out.text = base64.b64encode(
                self.inp.text.encode('utf-8')).decode('utf-8')
        except Exception as e:
            self.out.text = f'Error: {e}'

    def decode_b64(self, *a):
        try:
            self.out.text = base64.b64decode(
                self.inp.text.encode('utf-8')).decode('utf-8')
        except Exception as e:
            self.out.text = f'Error: {e}'

    def url_encode(self, *a):
        try:
            from urllib.parse import quote
            self.out.text = quote(self.inp.text, safe='')
        except Exception as e:
            self.out.text = f'Error: {e}'

    def url_decode(self, *a):
        try:
            from urllib.parse import unquote
            self.out.text = unquote(self.inp.text)
        except Exception as e:
            self.out.text = f'Error: {e}'


# ══════════════════════════════════════════════════════
#  WORLD CLOCK  ★ جديد
# ══════════════════════════════════════════════════════
class WorldClockScreen(Screen):
    ZONES = [
        ('بغداد / مكة',       3),
        ('الرياض / دبي',      3),
        ('لندن (GMT)',         0),
        ('باريس (CET)',        1),
        ('موسكو (MSK)',        3),
        ('دبي (GST)',          4),
        ('كراتشي (PKT)',       5),
        ('الهند (IST)',        5.5),
        ('بكين (CST)',         8),
        ('طوكيو (JST)',        9),
        ('سيدني (AEST)',       10),
        ('نيويورك (EST)',     -5),
        ('لوس أنجلوس (PST)', -8),
        ('ساو باولو (BRT)',   -3),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._clock_ev     = None
        self.time_labels   = {}
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header(
            ar('الساعة العالمية 🌍'),
            back_cb=lambda x: self._go_back()))

        scroll = ScrollView(pos_hint={'x': 0, 'y': 0}, size_hint=(1, 0.93))
        box    = BoxLayout(orientation='vertical', size_hint_y=None,
                           spacing=dp(6), padding=dp(10))
        box.bind(minimum_height=box.setter('height'))

        for name, _ in self.ZONES:
            row = BoxLayout(size_hint_y=None, height=dp(52),
                            spacing=dp(8), padding=dp(8))
            bg(row, C['card'], radius=8)
            name_lbl = lbl(ar(name), size=13, color=C['purple'],
                           halign='right', size_hint=(0.55, 1))
            time_lbl = lbl('--:--:--', size=20, color=C['gold'],
                            bold=True, halign='left', size_hint=(0.45, 1))
            row.add_widget(name_lbl)
            row.add_widget(time_lbl)
            self.time_labels[name] = time_lbl
            box.add_widget(row)

        scroll.add_widget(box)
        root.add_widget(scroll)
        self.add_widget(root)

    def _go_back(self):
        if self._clock_ev:
            self._clock_ev.cancel()
        go_back(self.manager)

    def on_enter(self):
        self.update_times()
        self._clock_ev = Clock.schedule_interval(lambda dt: self.update_times(), 1)

    def on_leave(self):
        if self._clock_ev:
            self._clock_ev.cancel()

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
    DISPLAY_NAMES = {
        'اول_ظل':       'أول ظل',
        'جيش_x10':      'جيش ×10',
        'جيش_x50':      'جيش ×50',
        'محارب_اسبوع':  'محارب الأسبوع',
        'سيد_الظل':     'سيد الظل',
        'حارس_الكود':   'حارس الكود',
        'بومة_الليل':   'بومة الليل',
        'قاتل_الرئيس':  'قاتل الرئيس',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header(
            ar('الإنجازات 🏆'),
            back_cb=lambda x: go_back(self.manager)))

        self.scroll = ScrollView(pos_hint={'x': 0, 'y': 0}, size_hint=(1, 0.93))
        self.al = BoxLayout(orientation='vertical', size_hint_y=None,
                            spacing=dp(8), padding=dp(10))
        self.al.bind(minimum_height=self.al.setter('height'))
        self.scroll.add_widget(self.al)
        root.add_widget(self.scroll)
        self.add_widget(root)

    def on_enter(self):
        self.al.clear_widgets()
        try:
            con  = sqlite3.connect(DB)
            c    = con.cursor()
            c.execute('SELECT * FROM achievements')
            achs = c.fetchall()
            con.close()
            for a in achs:
                earned = a[3]
                card   = BoxLayout(size_hint_y=None, height=dp(72),
                                   spacing=dp(8), padding=dp(10))
                bg(card, (0.05, 0.15, 0.05, 0.9) if earned else C['card'], radius=10)
                info   = BoxLayout(orientation='vertical')
                disp_name = self.DISPLAY_NAMES.get(a[1], a[1])
                prefix    = '✅ ' if earned else '🔒 '
                info.add_widget(lbl(ar(prefix + disp_name), size=14, bold=True,
                                    color=C['gold'] if earned else C['sub'],
                                    halign='right'))
                info.add_widget(lbl(ar(a[2]), size=11,
                                    color=C['text'], halign='right'))
                if earned and a[4]:
                    info.add_widget(lbl(ar(f'بتاريخ: {a[4]}'), size=10,
                                        color=C['green'], halign='right'))
                card.add_widget(info)
                self.al.add_widget(card)
        except Exception:
            pass


# ══════════════════════════════════════════════════════
#  SHADOW ARMY
# ══════════════════════════════════════════════════════
class ArmyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        make_screen_bg(self)
        root.add_widget(make_header(
            ar('جيش الظل 👥'),
            back_cb=lambda x: go_back(self.manager)))

        card = BoxLayout(orientation='vertical',
                         pos_hint={'center_x': 0.5, 'center_y': 0.60},
                         size_hint=(0.88, None), height=dp(225),
                         padding=dp(15), spacing=dp(10))
        bg(card, C['card'], radius=14)
        self.army_lbl   = lbl(ar('الجيش: 0'),       size=30, color=C['purple'], bold=True)
        self.rank_lbl   = lbl(ar('الرتبة: E'),       size=20, color=C['gold'])
        self.level_lbl  = lbl(ar('المستوى: 1'),      size=16, color=C['text'])
        self.streak_lbl = lbl(ar('السلسلة: 0 يوم'),  size=14, color=C['green'])
        self.id_lbl     = lbl('Shadow ID: ...',       size=12, color=C['sub'])
        self.xp_bar     = ProgressBar(max=100, value=0, size_hint=(1, None), height=dp(12))
        for w in [self.army_lbl, self.rank_lbl, self.level_lbl,
                  self.streak_lbl, self.id_lbl, self.xp_bar]:
            card.add_widget(w)
        root.add_widget(card)

        root.add_widget(lbl(ar('متطلبات الرتبة التالية:'), size=13, color=C['purple'],
                            pos_hint={'center_x': 0.5, 'center_y': 0.27},
                            size_hint=(0.88, None), height=dp(25)))
        self.next_info = lbl('', size=12, color=C['text'],
                             pos_hint={'center_x': 0.5, 'center_y': 0.20},
                             size_hint=(0.88, None), height=dp(45), halign='center')
        root.add_widget(self.next_info)
        self.add_widget(root)

    def on_enter(self):
        try:
            p = get_profile()
            self.army_lbl.text   = ar(f'الجيش: {p["army"]}')
            self.rank_lbl.text   = ar(f'الرتبة: {p["rank"]}')
            self.rank_lbl.color  = RANK_COLORS.get(p['rank'], C['gold'])
            self.level_lbl.text  = ar(f'المستوى: {p["level"]}')
            self.streak_lbl.text = ar(f'السلسلة: {p["streak"]} يوم')
            self.id_lbl.text     = f'Shadow ID: {p["shadow_id"]}'
            xp_need = p['level'] * 100
            self.xp_bar.max   = xp_need
            self.xp_bar.value = p['xp']
            nexts = {
                'E': ar('ابلغ المستوى 5  ←  رتبة D'),
                'D': ar('ابلغ المستوى 10 ←  رتبة C'),
                'C': ar('ابلغ المستوى 20 ←  رتبة B'),
                'B': ar('ابلغ المستوى 35 ←  رتبة A'),
                'A': ar('ابلغ المستوى 50 ←  رتبة S'),
                'S': ar('أعلى رتبة تم بلوغها! 👑'),
            }
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
        root.add_widget(make_header(
            ar('مخزن المهارات ⚡'),
            back_cb=lambda x: go_back(self.manager)))

        self.scroll = ScrollView(pos_hint={'x': 0, 'y': 0}, size_hint=(1, 0.93))
        self.sl = BoxLayout(orientation='vertical', size_hint_y=None,
                            spacing=dp(8), padding=dp(10))
        self.sl.bind(minimum_height=self.sl.setter('height'))
        self.scroll.add_widget(self.sl)
        root.add_widget(self.scroll)
        self.add_widget(root)

    def on_enter(self):
        self.sl.clear_widgets()
        try:
            p     = get_profile()
            rank  = p.get('rank', 'E')
            level = p.get('level', 1)
            skills = [
                ('خطوة الظل',   'E',  1,  'حركة أساسية في الظلام'),
                ('رداء الظل',   'E',  3,  'احجب كل مشتتات الانتباه'),
                ('رؤية الظلام', 'D',  5,  'شاهد الفرص التي يفوتها الآخرون'),
                ('جيش الظل',    'D',  8,  'قد جيش مهامك'),
                ('ضربة الفراغ', 'C',  12, 'أنجز المهام في لحظة'),
                ('مجال الظل',   'C',  18, 'سيطر على بيئتك الكاملة'),
                ('إرادة الملك', 'B',  25, 'اثنِ الواقع نحو أهدافك'),
                ('انهض!',       'A',  40, 'استدعِ أقصى إنتاجيتك'),
                ('ملك الظل',    'S',  50, 'القوة المطلقة مفعّلة'),
            ]
            rank_order = ['E', 'D', 'C', 'B', 'A', 'S']
            for name, req_rank, req_lvl, desc in skills:
                unlocked = (rank_order.index(rank) >= rank_order.index(req_rank)
                            and level >= req_lvl)
                card = BoxLayout(size_hint_y=None, height=dp(72),
                                 spacing=dp(8), padding=dp(10))
                bg(card, (0.05, 0.12, 0.05, 0.9) if unlocked else C['card2'], radius=10)
                info = BoxLayout(orientation='vertical')
                pfx  = '⚡ ' if unlocked else '🔒 '
                info.add_widget(lbl(ar(pfx + name), size=14, bold=True,
                                    color=C['gold'] if unlocked else C['sub'],
                                    halign='right'))
                info.add_widget(lbl(ar(desc), size=11, color=C['text'], halign='right'))
                req = lbl(ar(f'رتبة {req_rank} | مستوى {req_lvl}'), size=10,
                           color=C['green'] if unlocked else C['red'],
                           size_hint=(None, 1), width=dp(110))
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
            Window.clearcolor = (0, 0, 0, 1)
            init_db()
            sm = ScreenManager(transition=FadeTransition(duration=0.3))
            screens = [
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
            ]
            for s in screens:
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
