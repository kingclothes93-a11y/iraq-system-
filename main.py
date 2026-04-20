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
        # تفعيل الوضع المظلم لزيادة الغموض
        self.theme_cls.theme_style = "Dark"
        
        # 1. شاشة الصمت (الافتتاحية الغامضة)
        # صورة عين جين وو المتوهجة وسط الظلام
        splash_url = "https://w0.peakpx.com/wallpaper/404/695/HD-wallpaper-sung-jin-woo-eye-glowing-blue-anime-solo-leveling.jpg"
        self.show_splash(splash_url)
        
        screen = MDScreen()
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # 2. الواجهة الداخلية (ظلال جين وو)
        # صورة جين وو وظلاله المهيبة تقف خلفه
        internal_url = "https://w0.peakpx.com/wallpaper/326/289/HD-wallpaper-sung-jin-woo-solo-leveling-anime-aesthetic-shadows.jpg"
        img = AsyncImage(
            source=internal_url,
            size_hint=(1, 0.7),
            allow_stretch=True,
            keep_ratio=False # ملء الشاشة تماماً لزيادة الهيبة
        )
        
        # تنسيق النص الملكي بالأزرق السماوي الحاد
        label = MDLabel(
            text="[SYSTEM]: Connection Established.\nWelcome, Shadow Monarch.",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0.8, 1, 1), # Cyan
            font_style="H5",
            bold=True
        )
        
        layout.add_widget(img)
        layout.add_widget(label)
        screen.add_widget(layout)
        return screen

    def show_splash(self, image_url):
        # شاشة سوداء تماماً خلف الصورة
        view = ModalView(auto_dismiss=False, background_color=(0, 0, 0, 1))
        splash_img = AsyncImage(source=image_url, allow_stretch=True, keep_ratio=False)
        view.add_widget(splash_img)
        view.open()
        # عرض الغموض لمدة 3 ثوانٍ
        Clock.schedule_once(lambda dt: view.dismiss(), 3)

if __name__ == "__main__":
    MainApp().run()
