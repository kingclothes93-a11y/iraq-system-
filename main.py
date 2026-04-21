from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

class TestApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        screen = MDScreen()
        screen.add_widget(MDLabel(text="SYSTEM ACTIVE - NO IMAGES", halign="center", font_style="H3"))
        return screen

TestApp().run()
