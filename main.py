import os
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

# --- ألوان ثيم ملك الظلال (Shadow Monarch) ---
C_BG = (0.02, 0.0, 0.06, 1)      # الخلفية السوداء المزرقة
C_PURPLE = (0.55, 0.0, 1.0, 1)  # البنفسجي الملكي
C_MENU_BG = (0.07, 0, 0.15, 1)  # خلفية القائمة الجانبية

class ShadowBtn(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0,0,0,0)
        with self.canvas.before:
            Color(*C_PURPLE)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
        self.bind(pos=self._upd, size=self._upd)
    def _upd(self, *args): self.rect.pos, self.rect.size = self.pos, self.size

# ─── شاشة الترحيب (البداية) ───
class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Label(text="SHADOW SYSTEM ACTIVE", font_size='25sp', color=C_PURPLE, pos_hint={'center_y': 0.5}))
        layout.add_widget(Label(text="Open Menu to Start", font_size='14sp', pos_hint={'center_y': 0.4}))
        self.add_widget(layout)

# ─── الحاوية الرئيسية (نظام القائمة ≡) ───
class MainContainer(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 1. مدير الشاشات (الحاوية اللي راح نحط بيها الأدوات مستقبلاً)
        self.sm = ScreenManager(transition=FadeTransition())
        self.sm.add_widget(WelcomeScreen(name='welcome'))
        self.add_widget(self.sm)

        # 2. القائمة الجانبية (Container)
        self.menu = BoxLayout(orientation='vertical', size_hint=(0.6, 1), pos_hint={'x': -0.6}, padding=dp(15), spacing=dp(10))
        with self.menu.canvas.before:
            Color(*C_MENU_BG)
            self.m_rect = Rectangle(pos=self.menu.pos, size=self.menu.size)
        self.menu.bind(pos=self._upd_m, size=self._upd_m)
        
        # عنوان القائمة
        self.menu.add_widget(Label(text="MENU", font_size='20sp', size_hint_y=None, height=dp(80), color=C_PURPLE))
        
        # زر تجريبي (راح نغيره لما نضيف أول أداة)
        btn_home = ShadowBtn(text="Home", size_hint_y=None, height=dp(50))
        btn_home.bind(on_release=lambda x: self.switch_to('welcome'))
        self.menu.add_widget(btn_home)
        
        self.add_widget(self.menu)

        # 3. زر القائمة العلوي (≡) اللي بالصورة مالتك
        self.m_btn = Button(text="≡", size_hint=(None,None), size=(dp(60),dp(60)), 
                             pos_hint={'top':1, 'right':1}, background_color=(0,0,0,0), 
                             font_size='40sp', color=C_PURPLE)
        self.m_btn.bind(on_release=self.toggle_menu)
        self.add_widget(self.m_btn)
        
        self.is_open = False

    def _upd_m(self, *args): self.m_rect.pos, self.m_rect.size = self.menu.pos, self.menu.size

    def toggle_menu(self, *args):
        # حركة فتح وغلق القائمة
        target_x = 0 if not self.is_open else -0.6
        Animation(pos_hint={'x': target_x}, duration=0.25).start(self.menu)
        self.is_open = not self.is_open

    def switch_to(self, screen_name):
        self.sm.current = screen_name
        self.toggle_menu()

class ShadowApp(App):
    def build(self):
        Window.clearcolor = C_BG
        return MainContainer()

if __name__ == '__main__':
    ShadowApp().run()
