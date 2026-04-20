import time
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.clock import Clock

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        
        # 1. شاشة الصمت (Splash Screen)
        # تأكد إنك سميت الصورة بـ GitHub (splash.jpg)
        splash_url = "https://raw.githubusercontent.com/kingclothes93-a11y/iraq-system-/main/splash.jpg"
        self.show_splash(splash_url)
        
        screen = MDScreen()
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # 2. الواجهة الداخلية
        # تأكد إنك سميت الصورة بـ GitHub (main.jpg)
        internal_url = "https://raw.githubusercontent.com/kingclothes93-a11y/iraq-system-/main/main.jpg"
        img = AsyncImage(
            source=internal_url,
            size_hint=(1, 0.7),
            allow_stretch=True
        )
        
        label = MDLabel(
            text="[SYSTEM]: Connection Established.\nWelcome, Shadow Monarch.",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0.8, 1, 1),
            font_style="H5"
        )
        
        layout.add_widget(img)
        layout.add_widget(label)
        screen.add_widget(layout)
        return screen

    def show_splash(self, image_url):
        view = ModalView(auto_dismiss=False, background_color=(0, 0, 0, 1))
        splash_img = AsyncImage(source=image_url, allow_stretch=True)
        view.add_widget(splash_img)
        view.open()
        Clock.schedule_once(lambda dt: view.dismiss(), 3)

if __name__ == "__main__":
    MainApp().run()
