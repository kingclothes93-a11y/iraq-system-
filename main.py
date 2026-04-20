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
        # إعدادات التصميم (Dark Mode)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        
        # 1. شاشة الواجهة (Splash Screen) - صورة الصمت
        splash_url = "https://raw.githubusercontent.com/kingclothes93-a11y/iraq-system-/main/solo_splash.jpg"
        self.show_splash(splash_url)
        
        # 2. الشاشة الداخلية (Main Screen)
        screen = MDScreen()
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # إضافة الصورة الداخلية (AsyncImage تحمل من النت) - صورة النظر ببرود
        internal_url = "https://raw.githubusercontent.com/kingclothes93-a11y/iraq-system-/main/solo_internal.jpg"
        img = AsyncImage(
            source=internal_url,
            size_hint=(1, 0.7), # تأخذ مساحة كبيرة
            allow_stretch=True
        )
        
        label = MDLabel(
            text="[SYSTEM]: Connection Established.\nWelcome, Shadow Monarch.",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0.8, 1, 1), # أزرق سستم
            font_style="H5"
        )
        
        layout.add_widget(img)
        layout.add_widget(label)
        screen.add_widget(layout)
        
        return screen

    def show_splash(self, image_url):
        # إنشاء نافذة مؤقتة للواجهة
        view = ModalView(auto_dismiss=False, background_color=(0, 0, 0, 1))
        
        # تحميل صورة الواجهة من الإنترنت
        splash_img = AsyncImage(source=image_url, allow_stretch=True)
        view.add_widget(splash_img)
        
        # فتح الواجهة
        view.open()
        
        # إغلاق الواجهة بعد 3 ثواني تلقائياً
        Clock.schedule_once(lambda dt: view.dismiss(), 3)

if __name__ == "__main__":
    MainApp().run()
