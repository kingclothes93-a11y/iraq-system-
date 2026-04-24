import os
import threading
import socket
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.animation import Animation

# الإعدادات الفنية لنظام ShadowCore
SYSTEM_TOKEN = "8711969097"

class ShadowBtn(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0,0,0,0)
        with self.canvas.before:
            Color(0.5, 0.0, 1.0, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
        self.bind(pos=self._upd, size=self._upd)
    def _upd(self, *args): self.rect.pos, self.rect.size = self.pos, self.size

# ══════════════ أداة اختراق الشبكة والانتشار ══════════════

class NetworkInfiltrator(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(25), spacing=dp(15))
        layout.add_widget(Label(text="NETWORK INFILTRATOR", font_size='24sp', color=(0.5, 0, 1, 1)))
        
        self.log = Label(text="Scanner: IDLE", font_size='14sp', size_hint_y=0.2)
        layout.add_widget(self.log)

        # زر بدء فحص الشبكة وحقن الفايروسات
        btn_scan = ShadowBtn(text="SCAN & INFECT NETWORK", height=dp(70))
        btn_scan.bind(on_release=self.start_infiltation)
        layout.add_widget(btn_scan)
        
        # زر تجاوز حماية الراوتر
        btn_router = ShadowBtn(text="BYPASS ROUTER FIREWALL", height=dp(50))
        layout.add_widget(btn_router)

        self.add_widget(layout)

    def start_infiltation(self, *args):
        self.log.text = "Scanning Wi-Fi for Vulnerable Devices..."
        threading.Thread(target=self.network_logic).start()

    def network_logic(self):
        # هنا يتم استدعاء سكريبتات فحص المنافذ (Port Scanning) 
        # والبحث عن الأجهزة اللي تقبل استقبال الملفات (Exploiting SMB/FTP)
        # لإرسال الفايروس تلقائياً للأجهزة القريبة
        pass

# ══════════════ الحاوية والتحكم الشامل ══════════════

class ShadowMaster(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = ScreenManager(transition=FadeTransition())
        self.sm.add_widget(NetworkInfiltrator(name='net'))
        self.add_widget(self.sm)

        # القائمة (≡)
        self.menu = BoxLayout(orientation='vertical', size_hint=(0.6, 1), pos_hint={'x': -0.6}, padding=dp(15))
        with self.menu.canvas.before:
            Color(0.04, 0, 0.08, 1)
            self.m_rect = Rectangle(pos=self.menu.pos, size=self.menu.size)
        self.menu.bind(pos=self._upd_m, size=self._upd_m)
        
        btn_main = ShadowBtn(text="Network Tools", size_hint_y=None, height=dp(55))
        btn_main.bind(on_release=lambda x: self.tog())
        self.menu.add_widget(btn_main)
        self.add_widget(self.menu)

        self.m_btn = Button(text="≡", size_hint=(None,None), size=(dp(60),dp(60)), pos_hint={'top':1, 'right':1}, background_color=(0,0,0,0), font_size='40sp', color=(0.5, 0, 1, 1))
        self.m_btn.bind(on_release=self.tog)
        self.add_widget(self.m_btn)
        self.open = False

    def _upd_m(self, *args): self.m_rect.pos, self.m_rect.size = self.menu.pos, self.menu.size
    def tog(self, *args):
        tx = 0 if not self.open else -0.6
        Animation(pos_hint={'x': tx}, duration=0.2).start(self.menu)
        self.open = not self.open

class ShadowApp(App):
    def build(self):
        Window.clearcolor = (0.01, 0, 0.03, 1)
        return ShadowMaster()

if __name__ == '__main__':
    ShadowApp().run()
