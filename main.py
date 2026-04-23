import sys
import traceback
import os
import ssl
import json
import datetime
import random
import string
import re
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
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.animation import Animation

Logger.setLevel('DEBUG')

NOTES_FILE = 'notes.json'
TASKS_FILE = 'tasks.json'
SNIPPETS_FILE = 'snippets.json'


def load_json(path):
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return []


def save_json(path, data):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except:
        pass


def styled_btn(text, bg=(0.25, 0.0, 0.55, 0.9), fg=(1,1,1,1),
               radius=10, font_size=15, markup=False, **kwargs):
    btn = Button(
        text=text, markup=markup,
        font_size=dp(font_size),
        background_color=(0,0,0,0),
        color=fg,
        background_normal='',
        **kwargs
    )
    with btn.canvas.before:
        Color(*bg)
        btn._bg = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[dp(radius)])
    btn.bind(
        pos=lambda i,v: setattr(i._bg,'pos',v),
        size=lambda i,v: setattr(i._bg,'size',v)
    )
    return btn


def make_header(title, back_screen=None):
    header = BoxLayout(pos_hint={'x':0,'top':1},
                       size_hint=(1, 0.07), padding=dp(10))
    with header.canvas.before:
        Color(0.08, 0.0, 0.2, 1)
        header._bg = Rectangle(pos=header.pos, size=header.size)
    header.bind(pos=lambda i,v: setattr(i._bg,'pos',v),
                size=lambda i,v: setattr(i._bg,'size',v))
    if back_screen:
        back = styled_btn('< Back', bg=(0,0,0,0), fg=(0.8,0.5,1,1),
                          size_hint=(None,1), width=dp(80))
        header.add_widget(back)
        header._back_btn = back
    header.add_widget(Label(text=f'[b]{title}[/b]', markup=True,
                            font_size=dp(17), color=(0.8,0.4,1,1)))
    return header


class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0.0, 0.0, 0.08, 1)
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg,'pos',v),
                    size=lambda i,v: setattr(self.bg,'size',v))

        self.title = Label(
            text='[b]MALIK DHALAL[/b]',
            markup=True,
            font_size=dp(38),
            color=(0.7, 0.0, 1.0, 0),
            pos_hint={'center_x': 0.5, 'center_y': 0.58},
            size_hint=(1, None), height=dp(60)
        )
        self.sub = Label(
            text='Dev System v2.0',
            font_size=dp(14),
            color=(0.6, 0.4, 1.0, 0),
            pos_hint={'center_x': 0.5, 'center_y': 0.48},
            size_hint=(1, None), height=dp(30)
        )
        self.bar_bg = FloatLayout(
            pos_hint={'center_x': 0.5, 'center_y': 0.35},
            size_hint=(0.7, None)
        )
        self.bar_bg.height = dp(4)
        with self.bar_bg.canvas:
            Color(0.2, 0.0, 0.4, 1)
            self.bar_bg_rect = Rectangle(pos=self.bar_bg.pos, size=self.bar_bg.size)
        self.bar_bg.bind(pos=lambda i,v: setattr(self.bar_bg_rect,'pos',v),
                         size=lambda i,v: setattr(self.bar_bg_rect,'size',v))

        layout.add_widget(self.title)
        layout.add_widget(self.sub)
        layout.add_widget(self.bar_bg)
        self.add_widget(layout)

    def on_enter(self):
        anim = Animation(color=(0.7,0.0,1.0,1), duration=0.8)
        anim.start(self.title)
        anim2 = Animation(color=(0.6,0.4,1.0,1), duration=0.8, t='out_cubic')
        Clock.schedule_once(lambda dt: anim2.start(self.sub), 0.3)
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'lock'), 2.2)


class LockScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        if os.path.exists('bg_lock.jpg'):
            bg = Image(source='bg_lock.jpg', allow_stretch=True,
                       keep_ratio=False, size_hint=(1,1), pos_hint={'x':0,'y':0})
            layout.add_widget(bg)
        else:
            with layout.canvas.before:
                Color(0.05, 0.0, 0.15, 1)
                self.bg = Rectangle(pos=layout.pos, size=layout.size)
            layout.bind(pos=lambda i,v: setattr(self.bg,'pos',v),
                        size=lambda i,v: setattr(self.bg,'size',v))

        overlay = FloatLayout(size_hint=(1,1), pos_hint={'x':0,'y':0})
        with overlay.canvas.before:
            Color(0,0,0,0.45)
            self.ov = Rectangle(pos=overlay.pos, size=overlay.size)
        overlay.bind(pos=lambda i,v: setattr(self.ov,'pos',v),
                     size=lambda i,v: setattr(self.ov,'size',v))

        title = Label(text='[b]MALIK DHALAL[/b]', markup=True,
                      font_size=dp(34), color=(0.7,0.0,1.0,1),
                      pos_hint={'center_x':0.5,'center_y':0.84},
                      size_hint=(1,None), height=dp(55))
        subtitle = Label(text='Dev System  |  Enter PIN',
                         font_size=dp(13), color=(0.75,0.5,1.0,0.85),
                         pos_hint={'center_x':0.5,'center_y':0.75},
                         size_hint=(1,None), height=dp(25))

        self.pin_display = Label(text='o  o  o  o  o',
                                 font_size=dp(26), color=(0.8,0.4,1.0,1),
                                 pos_hint={'center_x':0.5,'center_y':0.62},
                                 size_hint=(1,None), height=dp(40))
        self.pin_entered = ''

        numpad = BoxLayout(orientation='vertical',
                           pos_hint={'center_x':0.5,'center_y':0.36},
                           size_hint=(0.72, 0.42), spacing=dp(8))

        for row in [['1','2','3'],['4','5','6'],['7','8','9'],['<','0','OK']]:
            row_layout = BoxLayout(orientation='horizontal', spacing=dp(8))
            for txt in row:
                is_ok = txt == 'OK'
                btn = styled_btn(
                    txt,
                    bg=(0.45,0.0,0.9,1) if is_ok else (0.2,0.0,0.5,0.9),
                    font_size=18
                )
                btn.bind(on_press=self.on_btn_press)
                row_layout.add_widget(btn)
            numpad.add_widget(row_layout)

        self.err = Label(text='', font_size=dp(13), color=(1,0.3,0.3,1),
                         pos_hint={'center_x':0.5,'center_y':0.10},
                         size_hint=(1,None), height=dp(30))

        for w in [title, subtitle, self.pin_display, numpad, self.err]:
            overlay.add_widget(w)
        layout.add_widget(overlay)
        self.add_widget(layout)

    def on_btn_press(self, btn):
        t = btn.text
        if t == '<':
            self.pin_entered = self.pin_entered[:-1]
        elif t == 'OK':
            if self.pin_entered == '20057':
                self.manager.transition = FadeTransition(duration=0.3)
                self.manager.current = 'main'
            else:
                self.err.text = 'Wrong PIN!'
                self.pin_entered = ''
                self.pin_display.text = 'o  o  o  o  o'
                Clock.schedule_once(lambda dt: setattr(self.err,'text',''), 2)
            return
        else:
            if len(self.pin_entered) < 5:
                self.pin_entered += t
        filled = '* ' * len(self.pin_entered)
        empty = 'o ' * (5 - len(self.pin_entered))
        self.pin_display.text = (filled + empty).strip()


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        if os.path.exists('bg_main.jpg'):
            bg = Image(source='bg_main.jpg', allow_stretch=True,
                       keep_ratio=False, size_hint=(1,1), pos_hint={'x':0,'y':0})
            layout.add_widget(bg)
        else:
            with layout.canvas.before:
                Color(0.0,0.0,0.05,1)
                self.bg = Rectangle(pos=layout.pos, size=layout.size)
            layout.bind(pos=lambda i,v: setattr(self.bg,'pos',v),
                        size=lambda i,v: setattr(self.bg,'size',v))

        overlay = FloatLayout(size_hint=(1,1), pos_hint={'x':0,'y':0})
        with overlay.canvas.before:
            Color(0,0,0,0.62)
            self.ov = Rectangle(pos=overlay.pos, size=overlay.size)
        overlay.bind(pos=lambda i,v: setattr(self.ov,'pos',v),
                     size=lambda i,v: setattr(self.ov,'size',v))

        header = BoxLayout(pos_hint={'x':0,'top':1},
                           size_hint=(1,0.08), padding=dp(12))
        with header.canvas.before:
            Color(0.08,0.0,0.2,0.95)
            self.hdr = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=lambda i,v: setattr(self.hdr,'pos',v),
                    size=lambda i,v: setattr(self.hdr,'size',v))
        header.add_widget(Label(text='[b]MALIK DHALAL[/b]  Dev System',
                                markup=True, font_size=dp(16),
                                color=(0.8,0.4,1.0,1)))

        self.clock_label = Label(font_size=dp(13), color=(0.7,0.7,0.9,1),
                                 pos_hint={'center_x':0.5,'center_y':0.89},
                                 size_hint=(1,None), height=dp(25))
        Clock.schedule_interval(self.update_clock, 1)

        scroll = ScrollView(pos_hint={'x':0,'y':0.0}, size_hint=(1,0.82))
        tools_layout = BoxLayout(orientation='vertical', size_hint_y=None,
                                 padding=dp(12), spacing=dp(10))
        tools_layout.bind(minimum_height=tools_layout.setter('height'))

        tools = [
            ('Notes',      'notes',    'Write & save notes',           (0.15,0.0,0.35)),
            ('Snippets',   'snippets', 'Save & copy code snippets',    (0.0,0.1,0.35)),
            ('Calculator', 'calc',     'Dev calc + HEX / BIN',         (0.1,0.0,0.3)),
            ('Tasks',      'tasks',    'Manage your dev tasks',         (0.2,0.0,0.25)),
            ('Pomodoro',   'pomodoro', '25min focus timer',             (0.3,0.05,0.1)),
            ('PassGen',    'passgen',  'Strong password generator',     (0.0,0.2,0.2)),
            ('Regex',      'regex',    'Test regex patterns live',      (0.05,0.1,0.3)),
            ('JSON',       'jsonf',    'Format & validate JSON',        (0.0,0.15,0.25)),
            ('Base Conv',  'baseconv', 'Dec / Hex / Bin / Oct',         (0.2,0.1,0.0)),
        ]

        for name, screen, desc, color in tools:
            btn = styled_btn(
                f'[b]{name}[/b]\n{desc}',
                bg=(color[0], color[1], color[2], 0.88),
                markup=True, font_size=15,
                size_hint_y=None, height=dp(70),
                halign='center'
            )
            btn.bind(on_press=lambda x, s=screen: self.go(s))
            tools_layout.add_widget(btn)

        scroll.add_widget(tools_layout)
        for w in [header, self.clock_label, scroll]:
            overlay.add_widget(w)
        layout.add_widget(overlay)
        self.add_widget(layout)

    def go(self, screen):
        self.manager.transition = SlideTransition(direction='left', duration=0.25)
        self.manager.current = screen

    def update_clock(self, dt):
        now = datetime.datetime.now()
        self.clock_label.text = now.strftime('%A  %H:%M:%S   %d/%m/%Y')


class NotesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notes = load_json(NOTES_FILE)
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0.03,0.0,0.1,1)
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg,'pos',v),
                    size=lambda i,v: setattr(self.bg,'size',v))

        header = make_header('Notes', back_screen='main')
        header._back_btn.bind(on_press=lambda x: self.go_back())
        layout.add_widget(header)

        self.scroll = ScrollView(pos_hint={'x':0,'y':0.18}, size_hint=(1,0.75))
        self.notes_layout = BoxLayout(orientation='vertical', size_hint_y=None,
                                      spacing=dp(8), padding=dp(10))
        self.notes_layout.bind(minimum_height=self.notes_layout.setter('height'))
        self.scroll.add_widget(self.notes_layout)
        layout.add_widget(self.scroll)

        input_area = BoxLayout(pos_hint={'x':0,'y':0}, size_hint=(1,0.17),
                               padding=dp(8), spacing=dp(8))
        self.note_input = TextInput(hint_text='Write a note...',
                                    background_color=(0.1,0.0,0.2,1),
                                    foreground_color=(1,1,1,1),
                                    cursor_color=(0.8,0.4,1,1), font_size=dp(14))
        add_btn = styled_btn('+', bg=(0.4,0.0,0.8,1), size_hint=(None,1), width=dp(50))
        add_btn.bind(on_press=self.add_note)
        input_area.add_widget(self.note_input)
        input_area.add_widget(add_btn)
        layout.add_widget(input_area)
        self.add_widget(layout)
        self.refresh_notes()

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.25)
        self.manager.current = 'main'

    def refresh_notes(self):
        self.notes_layout.clear_widgets()
        for i, note in enumerate(reversed(self.notes)):
            row = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(8), padding=dp(6))
            with row.canvas.before:
                Color(0.12,0.0,0.28,0.95)
                row._bg = RoundedRectangle(pos=row.pos, size=row.size, radius=[dp(8)])
            row.bind(pos=lambda i,v: setattr(i._bg,'pos',v),
                     size=lambda i,v: setattr(i._bg,'size',v))
            lbl = Label(text=note['text'][:60]+('...' if len(note['text'])>60 else ''),
                        font_size=dp(13), color=(0.9,0.9,0.9,1),
                        text_size=(Window.width*0.55, None), halign='left')
            del_btn = styled_btn('X', bg=(0.5,0.0,0.1,1), size_hint=(None,1), width=dp(40))
            idx = len(self.notes)-1-i
            del_btn.bind(on_press=lambda x, idx=idx: self.delete_note(idx))
            row.add_widget(lbl)
            row.add_widget(del_btn)
            self.notes_layout.add_widget(row)

    def add_note(self, *args):
        text = self.note_input.text.strip()
        if text:
            self.notes.append({'text': text,
                                'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})
            save_json(NOTES_FILE, self.notes)
            self.note_input.text = ''
            self.refresh_notes()

    def delete_note(self, idx):
        if 0 <= idx < len(self.notes):
            self.notes.pop(idx)
            save_json(NOTES_FILE, self.notes)
            self.refresh_notes()


class SnippetsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.snippets = load_json(SNIPPETS_FILE)
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0.03,0.0,0.1,1)
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg,'pos',v),
                    size=lambda i,v: setattr(self.bg,'size',v))

        header = make_header('Code Snippets', back_screen='main')
        header._back_btn.bind(on_press=lambda x: self.go_back())
        layout.add_widget(header)

        self.scroll = ScrollView(pos_hint={'x':0,'y':0.25}, size_hint=(1,0.68))
        self.snip_layout = BoxLayout(orientation='vertical', size_hint_y=None,
                                     spacing=dp(8), padding=dp(10))
        self.snip_layout.bind(minimum_height=self.snip_layout.setter('height'))
        self.scroll.add_widget(self.snip_layout)
        layout.add_widget(self.scroll)

        input_area = BoxLayout(pos_hint={'x':0,'y':0}, size_hint=(1,0.24),
                               padding=dp(8), spacing=dp(6), orientation='vertical')
        self.title_input = TextInput(hint_text='Title...', multiline=False,
                                     background_color=(0.1,0.0,0.2,1),
                                     foreground_color=(1,1,1,1),
                                     size_hint_y=None, height=dp(38), font_size=dp(13))
        self.code_input = TextInput(hint_text='Paste code here...',
                                    background_color=(0.05,0.0,0.15,1),
                                    foreground_color=(0.5,1.0,0.5,1), font_size=dp(12))
        save_btn = styled_btn('Save Snippet', bg=(0.3,0.0,0.7,1),
                              size_hint_y=None, height=dp(35))
        save_btn.bind(on_press=self.add_snippet)
        input_area.add_widget(self.title_input)
        input_area.add_widget(self.code_input)
        input_area.add_widget(save_btn)
        layout.add_widget(input_area)
        self.add_widget(layout)
        self.refresh_snippets()

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.25)
        self.manager.current = 'main'

    def refresh_snippets(self):
        self.snip_layout.clear_widgets()
        for i, snip in enumerate(reversed(self.snippets)):
            card = BoxLayout(size_hint_y=None, height=dp(72), spacing=dp(8), padding=dp(8))
            with card.canvas.before:
                Color(0.08,0.0,0.2,0.95)
                card._bg = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(8)])
            card.bind(pos=lambda i,v: setattr(i._bg,'pos',v),
                      size=lambda i,v: setattr(i._bg,'size',v))
            info = BoxLayout(orientation='vertical')
            info.add_widget(Label(text=snip.get('title','Snippet'), font_size=dp(13),
                                  bold=True, color=(0.8,0.5,1,1), halign='left'))
            info.add_widget(Label(text=snip.get('code','')[:40]+'...',
                                  font_size=dp(11), color=(0.4,1,0.4,1), halign='left'))
            copy_btn = styled_btn('Copy', bg=(0.0,0.35,0.15,1),
                                  size_hint=(None,1), width=dp(55))
            copy_btn.bind(on_press=lambda x, s=snip: Clipboard.copy(s.get('code','')))
            idx = len(self.snippets)-1-i
            del_btn = styled_btn('X', bg=(0.5,0.0,0.1,1), size_hint=(None,1), width=dp(35))
            del_btn.bind(on_press=lambda x, idx=idx: self.delete_snippet(idx))
            card.add_widget(info)
            card.add_widget(copy_btn)
            card.add_widget(del_btn)
            self.snip_layout.add_widget(card)

    def add_snippet(self, *args):
        title = self.title_input.text.strip()
        code = self.code_input.text.strip()
        if title and code:
            self.snippets.append({'title': title, 'code': code})
            save_json(SNIPPETS_FILE, self.snippets)
            self.title_input.text = ''
            self.code_input.text = ''
            self.refresh_snippets()

    def delete_snippet(self, idx):
        if 0 <= idx < len(self.snippets):
            self.snippets.pop(idx)
            save_json(SNIPPETS_FILE, self.snippets)
            self.refresh_snippets()


class CalcScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.expr = ''
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0.03,0.0,0.1,1)
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg,'pos',v),
                    size=lambda i,v: setattr(self.bg,'size',v))

        header = make_header('Dev Calculator', back_screen='main')
        header._back_btn.bind(on_press=lambda x: self.go_back())
        layout.add_widget(header)

        self.display = Label(text='0', font_size=dp(30), color=(1,1,1,1),
                             pos_hint={'center_x':0.5,'center_y':0.79},
                             size_hint=(0.92,None), height=dp(55), halign='right')
        self.sub_display = Label(text='', font_size=dp(12), color=(0.6,0.6,0.8,1),
                                 pos_hint={'center_x':0.5,'center_y':0.71},
                                 size_hint=(0.92,None), height=dp(22), halign='right')
        layout.add_widget(self.display)
        layout.add_widget(self.sub_display)

        grid = GridLayout(cols=4, pos_hint={'center_x':0.5,'center_y':0.36},
                          size_hint=(0.95,0.54), spacing=dp(6))
        btns = [
            ('C',(0.4,0.0,0.1,1)), ('()',(0.2,0.0,0.4,1)),
            ('%',(0.2,0.0,0.4,1)), ('/',(0.35,0.0,0.7,1)),
            ('7',None),('8',None),('9',None),('*',(0.35,0.0,0.7,1)),
            ('4',None),('5',None),('6',None),('-',(0.35,0.0,0.7,1)),
            ('1',None),('2',None),('3',None),('+',(0.35,0.0,0.7,1)),
            ('HEX',(0.0,0.2,0.4,1)),('0',None),('.',(0.15,0.0,0.3,1)),
            ('=',(0.5,0.0,0.9,1)),
        ]
        for txt, color in btns:
            btn = styled_btn(txt, bg=color if color else (0.15,0.0,0.35,1), font_size=16)
            btn.bind(on_press=self.on_calc)
            grid.add_widget(btn)
        layout.add_widget(grid)
        self.add_widget(layout)

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.25)
        self.manager.current = 'main'

    def on_calc(self, btn):
        t = btn.text
        if t == 'C':
            self.expr = ''
            self.display.text = '0'
            self.sub_display.text = ''
        elif t == '=':
            try:
                result = eval(self.expr)
                self.sub_display.text = self.expr
                self.display.text = str(result)
                self.expr = str(result)
            except:
                self.display.text = 'Error'
                self.expr = ''
        elif t == 'HEX':
            try:
                val = int(eval(self.expr))
                self.sub_display.text = f'HEX:{hex(val)}  BIN:{bin(val)}  OCT:{oct(val)}'
            except:
                self.sub_display.text = 'Not integer'
        elif t == '()':
            self.expr += '('
            self.display.text = self.expr
        else:
            self.expr += t
            self.display.text = self.expr


class TasksScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tasks = load_json(TASKS_FILE)
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0.03,0.0,0.1,1)
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg,'pos',v),
                    size=lambda i,v: setattr(self.bg,'size',v))

        header = make_header('Tasks', back_screen='main')
        header._back_btn.bind(on_press=lambda x: self.go_back())
        layout.add_widget(header)

        self.scroll = ScrollView(pos_hint={'x':0,'y':0.15}, size_hint=(1,0.78))
        self.tasks_layout = BoxLayout(orientation='vertical', size_hint_y=None,
                                      spacing=dp(8), padding=dp(10))
        self.tasks_layout.bind(minimum_height=self.tasks_layout.setter('height'))
        self.scroll.add_widget(self.tasks_layout)
        layout.add_widget(self.scroll)

        input_area = BoxLayout(pos_hint={'x':0,'y':0}, size_hint=(1,0.14),
                               padding=dp(8), spacing=dp(8))
        self.task_input = TextInput(hint_text='New task...', multiline=False,
                                    background_color=(0.1,0.0,0.2,1),
                                    foreground_color=(1,1,1,1), font_size=dp(14))
        add_btn = styled_btn('+', bg=(0.4,0.0,0.8,1), size_hint=(None,1), width=dp(50))
        add_btn.bind(on_press=self.add_task)
        input_area.add_widget(self.task_input)
        input_area.add_widget(add_btn)
        layout.add_widget(input_area)
        self.add_widget(layout)
        self.refresh_tasks()

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.25)
        self.manager.current = 'main'

    def refresh_tasks(self):
        self.tasks_layout.clear_widgets()
        for i, task in enumerate(self.tasks):
            done = task.get('done', False)
            row = BoxLayout(size_hint_y=None, height=dp(55), spacing=dp(8), padding=dp(8))
            with row.canvas.before:
                Color(0.05,0.2,0.05,0.9) if done else Color(0.12,0.0,0.28,0.95)
                row._bg = RoundedRectangle(pos=row.pos, size=row.size, radius=[dp(8)])
            row.bind(pos=lambda i,v: setattr(i._bg,'pos',v),
                     size=lambda i,v: setattr(i._bg,'size',v))
            lbl = Label(
                text=('[s]'+task['text']+'[/s]') if done else task['text'],
                markup=True, font_size=dp(13),
                color=(0.5,0.9,0.5,1) if done else (0.9,0.9,0.9,1),
                halign='left', text_size=(Window.width*0.55, None))
            done_btn = styled_btn('v' if not done else 'o',
                                  bg=(0.0,0.5,0.2,1) if not done else (0.2,0.2,0.2,1),
                                  size_hint=(None,1), width=dp(40))
            done_btn.bind(on_press=lambda x, idx=i: self.toggle_task(idx))
            del_btn = styled_btn('X', bg=(0.5,0.0,0.1,1), size_hint=(None,1), width=dp(35))
            del_btn.bind(on_press=lambda x, idx=i: self.delete_task(idx))
            row.add_widget(lbl)
            row.add_widget(done_btn)
            row.add_widget(del_btn)
            self.tasks_layout.add_widget(row)

    def add_task(self, *args):
        text = self.task_input.text.strip()
        if text:
            self.tasks.append({'text': text, 'done': False})
            save_json(TASKS_FILE, self.tasks)
            self.task_input.text = ''
            self.refresh_tasks()

    def toggle_task(self, idx):
        if 0 <= idx < len(self.tasks):
            self.tasks[idx]['done'] = not self.tasks[idx]['done']
            save_json(TASKS_FILE, self.tasks)
            self.refresh_tasks()

    def delete_task(self, idx):
        if 0 <= idx < len(self.tasks):
            self.tasks.pop(idx)
            save_json(TASKS_FILE, self.tasks)
            self.refresh_tasks()


class PomodoroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.work_min = 25
        self.break_min = 5
        self.seconds_left = self.work_min * 60
        self.running = False
        self.is_break = False
        self.sessions = 0
        self._clock = None

        layout = FloatLayout()
        with layout.canvas.before:
            Color(0.05,0.0,0.08,1)
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg,'pos',v),
                    size=lambda i,v: setattr(self.bg,'size',v))

        header = make_header('Pomodoro Timer', back_screen='main')
        header._back_btn.bind(on_press=lambda x: self.go_back())
        layout.add_widget(header)

        self.mode_label = Label(text='FOCUS', font_size=dp(16),
                                color=(1,0.4,0.4,1),
                                pos_hint={'center_x':0.5,'center_y':0.78},
                                size_hint=(1,None), height=dp(25))
        self.timer_label = Label(text='25:00', font_size=dp(60),
                                 bold=True, color=(1,1,1,1),
                                 pos_hint={'center_x':0.5,'center_y':0.65},
                                 size_hint=(1,None), height=dp(80))
        self.session_label = Label(text='Sessions: 0', font_size=dp(13),
                                   color=(0.6,0.6,0.8,1),
                                   pos_hint={'center_x':0.5,'center_y':0.54},
                                   size_hint=(1,None), height=dp(25))

        btns = BoxLayout(pos_hint={'center_x':0.5,'center_y':0.42},
                         size_hint=(0.8,None), height=dp(55), spacing=dp(12))
        self.start_btn = styled_btn('START', bg=(0.0,0.5,0.2,1), font_size=18)
        self.start_btn.bind(on_press=self.toggle_timer)
        reset_btn = styled_btn('RESET', bg=(0.4,0.0,0.1,1), font_size=18)
        reset_btn.bind(on_press=self.reset_timer)
        btns.add_widget(self.start_btn)
        btns.add_widget(reset_btn)

        skip_btn = styled_btn('Skip to Break', bg=(0.2,0.1,0.0,1),
                              size_hint=(0.5,None), height=dp(40),
                              pos_hint={'center_x':0.5,'center_y':0.31})
        skip_btn.bind(on_press=self.skip_phase)

        for w in [self.mode_label, self.timer_label, self.session_label, btns, skip_btn]:
            layout.add_widget(w)
        self.add_widget(layout)

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.25)
        self.manager.current = 'main'

    def toggle_timer(self, *args):
        if self.running:
            self.running = False
            if self._clock:
                self._clock.cancel()
            self.start_btn.text = 'START'
        else:
            self.running = True
            self._clock = Clock.schedule_interval(self.tick, 1)
            self.start_btn.text = 'PAUSE'

    def tick(self, dt):
        if self.seconds_left > 0:
            self.seconds_left -= 1
            m, s = divmod(self.seconds_left, 60)
            self.timer_label.text = f'{m:02d}:{s:02d}'
        else:
            if not self.is_break:
                self.sessions += 1
                self.session_label.text = f'Sessions: {self.sessions}'
                self.is_break = True
                self.seconds_left = self.break_min * 60
                self.mode_label.text = 'BREAK'
                self.mode_label.color = (0.4,1,0.4,1)
            else:
                self.is_break = False
                self.seconds_left = self.work_min * 60
                self.mode_label.text = 'FOCUS'
                self.mode_label.color = (1,0.4,0.4,1)

    def reset_timer(self, *args):
        self.running = False
        if self._clock:
            self._clock.cancel()
        self.is_break = False
        self.seconds_left = self.work_min * 60
        self.timer_label.text = '25:00'
        self.mode_label.text = 'FOCUS'
        self.mode_label.color = (1,0.4,0.4,1)
        self.start_btn.text = 'START'

    def skip_phase(self, *args):
        self.seconds_left = 0


class PassGenScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0.03,0.0,0.1,1)
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg,'pos',v),
                    size=lambda i,v: setattr(self.bg,'size',v))

        header = make_header('Password Generator', back_screen='main')
        header._back_btn.bind(on_press=lambda x: self.go_back())
        layout.add_widget(header)

        self.result = Label(text='Press Generate', font_size=dp(18),
                            color=(0.6,1,0.6,1),
                            pos_hint={'center_x':0.5,'center_y':0.72},
                            size_hint=(0.9,None), height=dp(45),
                            halign='center')

        self.length_label = Label(text='Length: 16', font_size=dp(14),
                                  color=(0.8,0.8,1,1),
                                  pos_hint={'center_x':0.5,'center_y':0.60},
                                  size_hint=(1,None), height=dp(25))
        self.slider = Slider(min=8, max=32, value=16, step=1,
                             pos_hint={'center_x':0.5,'center_y':0.52},
                             size_hint=(0.85,None), height=dp(40))
        self.slider.bind(value=self.on_slider)

        opts_layout = BoxLayout(pos_hint={'center_x':0.5,'center_y':0.41},
                                size_hint=(0.85,None), height=dp(40), spacing=dp(8))
        self.inc_upper = True
        self.inc_digits = True
        self.inc_symbols = True

        self.btn_upper = styled_btn('ABC', bg=(0.2,0.0,0.5,1), font_size=13)
        self.btn_digits = styled_btn('123', bg=(0.2,0.0,0.5,1), font_size=13)
        self.btn_symbols = styled_btn('#@!', bg=(0.2,0.0,0.5,1), font_size=13)
        self.btn_upper.bind(on_press=lambda x: self.toggle_opt('upper'))
        self.btn_digits.bind(on_press=lambda x: self.toggle_opt('digits'))
        self.btn_symbols.bind(on_press=lambda x: self.toggle_opt('symbols'))
        opts_layout.add_widget(self.btn_upper)
        opts_layout.add_widget(self.btn_digits)
        opts_layout.add_widget(self.btn_symbols)

        gen_btn = styled_btn('GENERATE', bg=(0.3,0.0,0.7,1), font_size=17,
                             size_hint=(0.6,None), height=dp(50),
                             pos_hint={'center_x':0.5,'center_y':0.28})
        gen_btn.bind(on_press=self.generate)

        copy_btn = styled_btn('Copy Password', bg=(0.0,0.35,0.15,1), font_size=14,
                              size_hint=(0.5,None), height=dp(40),
                              pos_hint={'center_x':0.5,'center_y':0.18})
        copy_btn.bind(on_press=lambda x: Clipboard.copy(self.result.text))

        for w in [self.result, self.length_label, self.slider,
                  opts_layout, gen_btn, copy_btn]:
            layout.add_widget(w)
        self.add_widget(layout)

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.25)
        self.manager.current = 'main'

    def on_slider(self, slider, val):
        self.length_label.text = f'Length: {int(val)}'

    def toggle_opt(self, opt):
        if opt == 'upper':
            self.inc_upper = not self.inc_upper
            self.btn_upper.color = (0,1,0,1) if self.inc_upper else (0.5,0.5,0.5,1)
        elif opt == 'digits':
            self.inc_digits = not self.inc_digits
            self.btn_digits.color = (0,1,0,1) if self.inc_digits else (0.5,0.5,0.5,1)
        elif opt == 'symbols':
            self.inc_symbols = not self.inc_symbols
            self.btn_symbols.color = (0,1,0,1) if self.inc_symbols else (0.5,0.5,0.5,1)

    def generate(self, *args):
        chars = string.ascii_lowercase
        if self.inc_upper:
            chars += string.ascii_uppercase
        if self.inc_digits:
            chars += string.digits
        if self.inc_symbols:
            chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
        length = int(self.slider.value)
        pwd = ''.join(random.choice(chars) for _ in range(length))
        self.result.text = pwd


class RegexScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0.03,0.0,0.1,1)
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg,'pos',v),
                    size=lambda i,v: setattr(self.bg,'size',v))

        header = make_header('Regex Tester', back_screen='main')
        header._back_btn.bind(on_press=lambda x: self.go_back())
        layout.add_widget(header)

        content = BoxLayout(orientation='vertical',
                            pos_hint={'x':0,'y':0}, size_hint=(1,0.93),
                            padding=dp(10), spacing=dp(8))

        content.add_widget(Label(text='Pattern:', font_size=dp(13),
                                 color=(0.7,0.5,1,1), size_hint_y=None, height=dp(22),
                                 halign='left'))
        self.pattern_input = TextInput(hint_text='e.g.  \\d+  or  [a-z]+',
                                       multiline=False,
                                       background_color=(0.1,0.0,0.2,1),
                                       foreground_color=(1,1,0,1),
                                       font_size=dp(14), size_hint_y=None, height=dp(42))
        content.add_widget(self.pattern_input)

        content.add_widget(Label(text='Test String:', font_size=dp(13),
                                 color=(0.7,0.5,1,1), size_hint_y=None, height=dp(22),
                                 halign='left'))
        self.test_input = TextInput(hint_text='Enter text to test...',
                                    background_color=(0.08,0.0,0.18,1),
                                    foreground_color=(1,1,1,1),
                                    font_size=dp(13), size_hint_y=None, height=dp(80))
        content.add_widget(self.test_input)

        test_btn = styled_btn('TEST', bg=(0.3,0.0,0.7,1), font_size=16,
                              size_hint_y=None, height=dp(45))
        test_btn.bind(on_press=self.test_regex)
        content.add_widget(test_btn)

        content.add_widget(Label(text='Matches:', font_size=dp(13),
                                 color=(0.7,0.5,1,1), size_hint_y=None, height=dp(22),
                                 halign='left'))
        self.result_label = Label(text='', font_size=dp(13),
                                  color=(0.4,1,0.4,1), halign='left',
                                  text_size=(Window.width-dp(20), None))
        content.add_widget(self.result_label)

        layout.add_widget(content)
        self.add_widget(layout)

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.25)
        self.manager.current = 'main'

    def test_regex(self, *args):
        try:
            pattern = self.pattern_input.text
            text = self.test_input.text
            matches = re.findall(pattern, text)
            if matches:
                self.result_label.color = (0.4,1,0.4,1)
                self.result_label.text = f'Found {len(matches)} match(es):\n' + '\n'.join(str(m) for m in matches[:10])
            else:
                self.result_label.color = (1,0.4,0.4,1)
                self.result_label.text = 'No matches found'
        except Exception as e:
            self.result_label.color = (1,0.6,0.0,1)
            self.result_label.text = f'Error: {str(e)}'


class JsonScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0.03,0.0,0.1,1)
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg,'pos',v),
                    size=lambda i,v: setattr(self.bg,'size',v))

        header = make_header('JSON Formatter', back_screen='main')
        header._back_btn.bind(on_press=lambda x: self.go_back())
        layout.add_widget(header)

        content = BoxLayout(orientation='vertical', pos_hint={'x':0,'y':0},
                            size_hint=(1,0.93), padding=dp(10), spacing=dp(8))
        self.input = TextInput(hint_text='Paste JSON here...',
                               background_color=(0.05,0.0,0.15,1),
                               foreground_color=(1,1,1,1), font_size=dp(12))
        btns = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(8))
        fmt_btn = styled_btn('Format', bg=(0.3,0.0,0.7,1), font_size=15)
        fmt_btn.bind(on_press=self.format_json)
        val_btn = styled_btn('Validate', bg=(0.0,0.3,0.15,1), font_size=15)
        val_btn.bind(on_press=self.validate_json)
        copy_btn = styled_btn('Copy', bg=(0.2,0.1,0.0,1), font_size=15)
        copy_btn.bind(on_press=lambda x: Clipboard.copy(self.input.text))
        btns.add_widget(fmt_btn)
        btns.add_widget(val_btn)
        btns.add_widget(copy_btn)
        self.status = Label(text='', font_size=dp(13), color=(0.4,1,0.4,1),
                            size_hint_y=None, height=dp(30))
        content.add_widget(self.input)
        content.add_widget(btns)
        content.add_widget(self.status)
        layout.add_widget(content)
        self.add_widget(layout)

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.25)
        self.manager.current = 'main'

    def format_json(self, *args):
        try:
            parsed = json.loads(self.input.text)
            self.input.text = json.dumps(parsed, indent=2, ensure_ascii=False)
            self.status.color = (0.4,1,0.4,1)
            self.status.text = 'Formatted!'
        except Exception as e:
            self.status.color = (1,0.4,0.4,1)
            self.status.text = f'Error: {str(e)}'

    def validate_json(self, *args):
        try:
            json.loads(self.input.text)
            self.status.color = (0.4,1,0.4,1)
            self.status.text = 'Valid JSON!'
        except Exception as e:
            self.status.color = (1,0.4,0.4,1)
            self.status.text = f'Invalid: {str(e)}'


class BaseConvScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0.03,0.0,0.1,1)
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg,'pos',v),
                    size=lambda i,v: setattr(self.bg,'size',v))

        header = make_header('Base Converter', back_screen='main')
        header._back_btn.bind(on_press=lambda x: self.go_back())
        layout.add_widget(header)

        content = BoxLayout(orientation='vertical', pos_hint={'x':0,'y':0},
                            size_hint=(1,0.93), padding=dp(15), spacing=dp(12))

        for label, attr, hint, color in [
            ('Decimal',     'dec', 'Enter decimal...', (1,1,1,1)),
            ('Hexadecimal', 'hex_i', 'Enter hex (e.g. FF)', (1,0.8,0,1)),
            ('Binary',      'bin_i', 'Enter binary (e.g. 1010)', (0.4,1,0.4,1)),
            ('Octal',       'oct_i', 'Enter octal...', (0.6,0.8,1,1)),
        ]:
            content.add_widget(Label(text=label, font_size=dp(13),
                                     color=(0.7,0.5,1,1), size_hint_y=None,
                                     height=dp(20), halign='left'))
            inp = TextInput(hint_text=hint, multiline=False,
                            background_color=(0.08,0.0,0.2,1),
                            foreground_color=color, font_size=dp(14),
                            size_hint_y=None, height=dp(42))
            setattr(self, attr, inp)
            content.add_widget(inp)

        conv_btn = styled_btn('CONVERT', bg=(0.35,0.0,0.75,1), font_size=17,
                              size_hint_y=None, height=dp(50))
        conv_btn.bind(on_press=self.convert)
        content.add_widget(conv_btn)

        layout.add_widget(content)
        self.add_widget(layout)

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.25)
        self.manager.current = 'main'

    def convert(self, *args):
        try:
            if self.dec.text:
                val = int(self.dec.text)
            elif self.hex_i.text:
                val = int(self.hex_i.text, 16)
            elif self.bin_i.text:
                val = int(self.bin_i.text, 2)
            elif self.oct_i.text:
                val = int(self.oct_i.text, 8)
            else:
                return
            self.dec.text = str(val)
            self.hex_i.text = hex(val)[2:].upper()
            self.bin_i.text = bin(val)[2:]
            self.oct_i.text = oct(val)[2:]
        except:
            self.dec.text = 'Error'


class MalekDhalalApp(App):
    def build(self):
        try:
            Window.clearcolor = (0,0,0,1)
            sm = ScreenManager(transition=FadeTransition(duration=0.3))
            sm.add_widget(SplashScreen(name='splash'))
            sm.add_widget(LockScreen(name='lock'))
            sm.add_widget(MainScreen(name='main'))
            sm.add_widget(NotesScreen(name='notes'))
            sm.add_widget(SnippetsScreen(name='snippets'))
            sm.add_widget(CalcScreen(name='calc'))
            sm.add_widget(TasksScreen(name='tasks'))
            sm.add_widget(PomodoroScreen(name='pomodoro'))
            sm.add_widget(PassGenScreen(name='passgen'))
            sm.add_widget(RegexScreen(name='regex'))
            sm.add_widget(JsonScreen(name='jsonf'))
            sm.add_widget(BaseConvScreen(name='baseconv'))
            sm.current = 'splash'
            return sm
        except Exception as e:
            Logger.error("App", traceback.format_exc())
            return Label(text=f'ERROR: {str(e)}')


if __name__ == '__main__':
    try:
        MalekDhalalApp().run()
    except Exception as e:
        Logger.critical("App", str(e))
        sys.exit(1)
