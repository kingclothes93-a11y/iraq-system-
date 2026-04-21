import os
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager, FadeTransition
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

class LockScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        # Load lock screen background (oardefault.jpg)
        try:
            if os.path.exists("oardefault.jpg"):
                layout.add_widget(Image(
                    source="oardefault.jpg", 
                    allow_stretch=True, 
                    keep_ratio=False
                ))
        except:
            pass
        
        self.add_widget(layout)
        
        # Status Text
        self.add_widget(MDLabel(
            text="SYSTEM LOCKED", 
            halign="center", 
            pos_hint={"center_y": 0.6}, 
            theme_text_color="Custom", 
            text_color=(0, 0.7, 1, 1),
            font_style="H4"
        ))
        
        # Access Button
        self.add_widget(MDRaisedButton(
            text="ENTER ACCESS CODE", 
            pos_hint={"center_x": 0.5, "center_y": 0.4}, 
            on_release=lambda x: self.open_system()
        ))

    def open_system(self):
        self.manager.current = "main"

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        # Load main background (wp14877560.webp)
        try:
            if os.path.exists("wp14877560.webp"):
                layout.add_widget(Image(
                    source="wp14877560.webp", 
                    allow_stretch=True, 
                    keep_ratio=False
                ))
        except:
            pass
            
        layout.add_widget(MDLabel(
            text="SHADOW MONARCH ACTIVE", 
            halign="center", 
            theme_text_color="Custom", 
            text_color=(0, 1, 0, 1),
            font_style="H5"
        ))
        self.add_widget(layout)

class ShadowApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        
        sm = MDScreenManager(transition=FadeTransition())
        sm.add_widget(LockScreen(name="lock"))
        sm.add_widget(MainScreen(name="main"))
        return sm

if __name__ == "__main__":
    ShadowApp().run()
