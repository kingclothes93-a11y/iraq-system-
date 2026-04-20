from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.uix.boxlayout import BoxLayout

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        screen = MDScreen()
        
        layout = BoxLayout(orientation
