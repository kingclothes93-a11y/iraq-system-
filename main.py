import sys
import traceback
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from kivy.logger import Logger
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window

Logger.setLevel('DEBUG')


class LockScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        if os.path.exists('bg_lock.jpg'):
            bg = Image(source='bg_lock.jpg', allow_stretch=True,
                      keep_ratio=False, size_hint=(1,1),
                      pos_hint={'x':0,'y':0})
            layout.add_widget(bg)
        else:
            with layout.canvas.before:
                Color(0.05, 0.0, 0.15, 1)
                self.bg = Rectangle(pos=layout.pos, size=layout.size)
            layout.bind(pos=lambda i,v: setattr(self.bg,'pos',v),
                       size=lambda i,v: setattr(self.bg,'size',v))

        overlay = FloatLayout(size_hint=(1,1), pos_hint={'x':0,'y':0})
        with overlay.canvas.before:
            Color(0, 0, 0, 0.4)
            self.ov = Rectangle(pos=overlay.pos, size=overlay.size)
        overlay.bind(pos=lambda i,v: setattr(self.ov,'pos',v),
                    size=lambda i,v: setattr(self.ov,'size',v))

        title = Label(
            text='مـلـك ضـلال',
            font_size=dp(40),
            bold=True,
            color=(0.7, 0.0, 1.0, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.82},
            size_hint=(1, None),
            height=dp(55)
        )

        subtitle = Label(
            text='النظام الشخصي',
            font_size=dp(15),
            color=(0.85, 0.6, 1.0, 0.9),
            pos_hint={'center_x': 0.5, 'center_y': 0.73},
            size_hint=(1, None),
            height=dp(28)
        )

        self.pin_display = Label(
            text='◦  ◦  ◦  ◦  ◦',
            font_size=dp(30),
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.59},
            size_hint=(1, None),
            height=dp(45)
        )

        self.pin_entered = ""

        numpad = BoxLayout(
            orientation='vertical',
            pos_hint={'center_x': 0.5, 'center_y': 0.34},
            size_hint=(0.65, 0.38),
            spacing=dp(7)
        )

        for row in [['1','2','3'],['4','5','6'],['7','8','9'],['⌫','0','✓']]:
            row_layout = BoxLayout(orientation='horizontal', spacing=dp(7))
            for txt in row:
                btn = Button(
                    text=txt,
                    font_size=dp(22),
                    background_color=(0,0,0,0),
                    color=(1,1,1,1),
                    background_normal=''
                )
                with btn.canvas.before:
                    Color(0.3, 0.0, 0.6, 0.85)
                    btn._bg = RoundedRectangle(
                        pos=btn.pos, size=btn.size, radius=[dp(8)])
                btn.bind(
                    pos=lambda i,v: setattr(i._bg,'pos',v),
                    size=lambda i,v: setattr(i._bg,'size',v)
                )
                btn.bind(on_press=self.on_press)
                row_layout.add_widget(btn)
            numpad.add_widget(row_layout)

        self.err = Label(
            text='',
            font_size=dp(14),
            color=(1, 0.3, 0.3, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.10},
            size_hint=(1, None),
            height=dp(30)
        )

        for w in [title, subtitle, self.pin_display, numpad, self.err]:
            overlay.add_widget(w)

        layout.add_widget(overlay)
        self.add_widget(layout)

    def on_press(self, btn):
        t = btn.text
        if t == '⌫':
            self.pin_entered = self.pin_entered[:-1]
        elif t == '✓':
            if self.pin_entered == '20057':
                self.manager.current = 'main'
            else:
                self.err.text = 'رمز خاطئ!'
                self.pin_entered = ''
                self.pin_display.text = '◦  ◦  ◦  ◦  ◦'
                Clock.schedule_once(
                    lambda dt: setattr(self.err, 'text', ''), 2)
            return
        else:
            if len(self.pin_entered) < 5:
                self.pin_entered += t

        dots = ('•  ' * len(self.pin_entered) +
                '◦  ' * (5 - len(self.pin_entered))).strip()
        self.pin_display.text = dots


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        if os.path.exists('bg_main.jpg'):
            bg = Image(source='bg_main.jpg', allow_stretch=True,
                      keep_ratio=False, size_hint=(1,1),
                      pos_hint={'x':0,'y':0})
            layout.add_widget(bg)
        else:
            with layout.canvas.before:
                Color(0.0, 0.0, 0.05, 1)
                self.bg = Rectangle(pos=layout.pos, size=layout.size)
            layout.bind(pos=lambda i,v: setattr(self.bg,'pos',v),
                       size=lambda i,v: setattr(self.bg,'size',v))

        overlay = FloatLayout(size_hint=(1,1), pos_hint={'x':0,'y':0})
        with overlay.canvas.before:
            Color(0, 0, 0, 0.55)
            self.ov = Rectangle(pos=overlay.pos, size=overlay.size)
        overlay.bind(pos=lambda i,v: setattr(self.ov,'pos',v),
                    size=lambda i,v: setattr(self.ov,'size',v))

        header = BoxLayout(
            pos_hint={'x':0,'top':1},
            size_hint=(1, 0.07),
            padding=dp(10)
        )
        with header.canvas.before:
            Color(0.1, 0.0, 0.25, 0.92)
            self.hdr = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=lambda i,v: setattr(self.hdr,'pos',v),
                    size=lambda i,v: setattr(self.hdr,'size',v))
        header.add_widget(Label(
            text='مـلـك ضـلال',
            font_size=dp(18),
            bold=True,
            color=(0.8, 0.4, 1.0, 1)
        ))

        tools_scroll = ScrollView(
            pos_hint={'x':0, 'y':0.07},
            size_hint=(1, 0.93)
        )
        tools_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(15),
            spacing=dp(12)
        )
        tools_layout.bind(minimum_height=tools_layout.setter('height'))

        tools = [
            ('📝', 'المفكرة', 'سجّل ملاحظاتك'),
            ('🔧', 'الأدوات', 'أدوات متعددة'),
            ('📊', 'الإحصائيات', 'عرض البيانات'),
            ('⚙️', 'الإعدادات', 'تخصيص التطبيق'),
        ]

        for icon, name, desc in tools:
            tool_btn = Button(
                text=f'{icon}  {name}\n{desc}',
                font_size=dp(16),
                background_color=(0,0,0,0),
                color=(1,1,1,1),
                background_normal='',
                size_hint_y=None,
                height=dp(70),
                halign='right'
            )
            with tool_btn.canvas.before:
                Color(0.2, 0.0, 0.4, 0.85)
                tool_btn._bg = RoundedRectangle(
                    pos=tool_btn.pos,
                    size=tool_btn.size,
                    radius=[dp(12)]
                )
            tool_btn.bind(
                pos=lambda i,v: setattr(i._bg,'pos',v),
                size=lambda i,v: setattr(i._bg,'size',v)
            )
            tools_layout.add_widget(tool_btn)

        tools_scroll.add_widget(tools_layout)

        for w in [header, tools_scroll]:
            overlay.add_widget(w)

        layout.add_widget(overlay)
        self.add_widget(layout)


class MalekDhalalApp(App):
    def build(self):
        try:
            Window.clearcolor = (0, 0, 0, 1)
            sm = ScreenManager(transition=FadeTransition(duration=0.2))
            sm.add_widget(LockScreen(name='lock'))
            sm.add_widget(MainScreen(name='main'))
            sm.current = 'lock'
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
