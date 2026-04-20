from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.uix.boxlayout import BoxLayout

class MainApp(MDApp):
    def build(self):
        # إعدادات الألوان
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        screen = MDScreen()
        
        # ترتيب العناصر
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        # نص ترحيبي
        label = MDLabel(
            text="King System يعمل بنجاح!",
            halign="center",
            theme_text_color="Primary",
            font_style="H4"
        )
        
        # زر بسيط
        button = MDRaisedButton(
            text="تم التثبيت بنجاح",
            pos_hint={"center_x": .5},
        )
        
        layout.add_widget(label)
        layout.add_widget(button)
        screen.add_widget(layout)
        
        return screen

if __name__ == "__main__":
    MainApp().run()
