import sys
import traceback
from kivy.logger import Logger
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.metrics import dp
import threading
import urllib.request
import urllib.parse
import json

Logger.setLevel('DEBUG')

ANTHROPIC_API_KEY = "YOUR_API_KEY_HERE"

class LockScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0.05, 0.0, 0.1, 1)
            self.bg_rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=self._update_rect, size=self._update_rect)

        title = Label(text='Shadow Monarch', font_size=dp(32), bold=True,
            color=(0.6, 0.0, 1.0, 1), pos_hint={'center_x': 0.5, 'center_y': 0.75},
            size_hint=(1, None), height=dp(50))

        subtitle = Label(text='النظام الشخصي', font_size=dp(16),
            color=(0.8, 0.5, 1.0, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.65},
            size_hint=(1, None), height=dp(30))

        self.pin_display = Label(text='◦ ◦ ◦ ◦ ◦', font_size=dp(28),
            color=(1, 1, 1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.52},
            size_hint=(1, None), height=dp(40))

        self.pin_entered = ""

        numpad_layout = BoxLayout(orientation='vertical',
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            size_hint=(0.7, 0.35), spacing=dp(8))

        for row in [['1','2','3'],['4','5','6'],['7','8','9'],['⌫','0','✓']]:
            row_layout = BoxLayout(orientation='horizontal', spacing=dp(8))
            for txt in row:
                btn = Button(text=txt, font_size=dp(22),
                    background_color=(0.2, 0.0, 0.4, 1),
                    color=(1, 1, 1, 1), background_normal='')
                btn.bind(on_press=self.on_num_press)
                row_layout.add_widget(btn)
            numpad_layout.add_widget(row_layout)

        self.error_label = Label(text='', font_size=dp(14),
            color=(1, 0.3, 0.3, 1), pos_hint={'center_x': 0.5, 'center_y': 0.12},
            size_hint=(1, None), height=dp(30))

        for w in [title, subtitle, self.pin_display, numpad_layout, self.error_label]:
            layout.add_widget(w)
        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def on_num_press(self, instance):
        txt = instance.text
        if txt == '⌫':
            self.pin_entered = self.pin_entered[:-1]
        elif txt == '✓':
            self.check_pin()
            return
        else:
            if len(self.pin_entered) < 5:
                self.pin_entered += txt
        dots = ('• ' * len(self.pin_entered) + '◦ ' * (5 - len(self.pin_entered))).strip()
        self.pin_display.text = dots

    def check_pin(self):
        if self.pin_entered == '20057':
            self.manager.current = 'main'
        else:
            self.error_label.text = 'رمز خاطئ! حاول مجدداً'
            self.pin_entered = ''
            self.pin_display.text = '◦ ◦ ◦ ◦ ◦'
            Clock.schedule_once(lambda dt: setattr(self.error_label, 'text', ''), 2)


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0.0, 0.0, 0.05, 1)
            self.bg_rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=self._update_rect, size=self._update_rect)

        header = BoxLayout(orientation='horizontal',
            pos_hint={'x': 0, 'top': 1}, size_hint=(1, 0.08), padding=dp(10))
        with header.canvas.before:
            Color(0.1, 0.0, 0.2, 1)
            self.header_rect = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=lambda i,v: setattr(self.header_rect,'pos',v),
                    size=lambda i,v: setattr(self.header_rect,'size',v))
        header.add_widget(Label(text='Shadow Monarch AI', font_size=dp(18),
            bold=True, color=(0.8, 0.4, 1.0, 1)))

        self.chat_scroll = ScrollView(pos_hint={'x':0,'y':0.12}, size_hint=(1,0.78))
        self.chat_layout = BoxLayout(orientation='vertical', size_hint_y=None,
            padding=dp(10), spacing=dp(8))
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.chat_scroll.add_widget(self.chat_layout)

        input_bar = BoxLayout(orientation='horizontal',
            pos_hint={'x':0,'y':0}, size_hint=(1,0.12), padding=dp(8), spacing=dp(8))
        with input_bar.canvas.before:
            Color(0.08, 0.0, 0.15, 1)
            self.input_rect = Rectangle(pos=input_bar.pos, size=input_bar.size)
        input_bar.bind(pos=lambda i,v: setattr(self.input_rect,'pos',v),
                       size=lambda i,v: setattr(self.input_rect,'size',v))

        self.text_input = TextInput(hint_text='اكتب رسالتك هنا...', font_size=dp(15),
            multiline=False, background_color=(0.15,0.0,0.3,1),
            foreground_color=(1,1,1,1), hint_text_color=(0.6,0.4,0.8,1),
            cursor_color=(1,1,1,1), size_hint=(0.8,1))
        self.text_input.bind(on_text_validate=self.send_message)

        send_btn = Button(text='إرسال', font_size=dp(15),
            background_color=(0.5,0.0,0.8,1), color=(1,1,1,1),
            background_normal='', size_hint=(0.2,1))
        send_btn.bind(on_press=self.send_message)

        input_bar.add_widget(self.text_input)
        input_bar.add_widget(send_btn)

        for w in [header, self.chat_scroll, input_bar]:
            layout.add_widget(w)
        self.add_widget(layout)

        self.conversation_history = []
        self.add_message('مرحباً! أنا مساعدك الذكي. كيف أقدر أساعدك؟', False)

    def _update_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def add_message(self, text, is_user=True):
        bubble_color = (0.3,0.0,0.6,1) if is_user else (0.1,0.05,0.2,1)
        prefix = 'أنت: ' if is_user else 'AI: '
        msg = Label(text=prefix+text, font_size=dp(14), color=(1,1,1,1),
            size_hint_y=None, text_size=(dp(280),None),
            halign='right' if is_user else 'left', valign='middle',
            padding=(dp(10),dp(8)))
        msg.bind(texture_size=lambda i,v: setattr(i,'height',v[1]+dp(16)))
        with msg.canvas.before:
            Color(*bubble_color)
            msg._bg = Rectangle(pos=msg.pos, size=msg.size)
        msg.bind(pos=lambda i,v: setattr(i._bg,'pos',v),
                 size=lambda i,v: setattr(i._bg,'size',v))
        self.chat_layout.add_widget(msg)
        Clock.schedule_once(lambda dt: setattr(self.chat_scroll,'scroll_y',0), 0.1)

    def send_message(self, instance):
        text = self.text_input.text.strip()
        if not text:
            return
        self.add_message(text, True)
        self.text_input.text = ''
        self.conversation_history.append({"role":"user","content":text})
        self.add_message('جاري التفكير...', False)
        t = threading.Thread(target=self.call_ai, args=(text,))
        t.daemon = True
        t.start()

    def call_ai(self, user_text):
        try:
            url = "https://api.anthropic.com/v1/messages"
            data = {
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 1024,
                "system": "أنت مساعد ذكي شخصي يتحدث العربية. أجب بشكل مختصر ومفيد.",
                "messages": self.conversation_history
            }
            req = urllib.request.Request(url,
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type':'application/json',
                         'x-api-key': ANTHROPIC_API_KEY,
                         'anthropic-version':'2023-06-01'},
                method='POST')
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                ai_reply = result['content'][0]['text']
        except Exception as e:
            ai_reply = f'خطأ: {str(e)}'
        self.conversation_history.append({"role":"assistant","content":ai_reply})
        Clock.schedule_once(lambda dt: self._update_ai_response(ai_reply), 0)

    def _update_ai_response(self, reply):
        if self.chat_layout.children:
            self.chat_layout.remove_widget(self.chat_layout.children[0])
        self.add_message(reply, False)


class ShadowMonarchApp(App):
    def build(self):
        try:
            sm = ScreenManager(transition=FadeTransition())
            sm.add_widget(LockScreen(name='lock'))
            sm.add_widget(MainScreen(name='main'))
            sm.current = 'lock'
            return sm
        except Exception as e:
            Logger.error("App", traceback.format_exc())
            return Label(text=f'ERROR: {str(e)}')

if __name__ == '__main__':
    try:
        ShadowMonarchApp().run()
    except Exception as e:
        Logger.critical("App", str(e))
        sys.exit(1)
