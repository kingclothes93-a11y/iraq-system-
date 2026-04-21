from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window

# This string contains the layout and design of your app
KV = '''
ScreenManager:
    LockScreen:
    MainScreen:

<LockScreen>:
    name: 'lock'
    MDFloatLayout:
        # Using the lock screen image you uploaded
        FitImage:
            source: 'oardefault.jpg'
        
        MDLabel:
            text: "SHADOW MONARCH"
            halign: "center"
            pos_hint: {"center_y": .8}
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            font_style: "H4"
            bold: True

        MDRaisedButton:
            text: "UNSEAL SYSTEM"
            pos_hint: {"center_x": .5, "center_y": .2}
            size_hint_x: .7
            on_release: root.manager.current = 'main'
            md_bg_color: 0.1, 0.1, 0.1, 1

<MainScreen>:
    name: 'main'
    MDFloatLayout:
        # Using the main screen image you uploaded
        FitImage:
            source: 'wp14877560.webp'
        
        MDLabel:
            text: "LEVELING SYSTEM ACTIVE"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0, 1, 0, 1
            font_style: "H5"
            pos_hint: {"center_y": .9}
            bold: True

        MDIconButton:
            icon: "shield-check"
            icon_size: "64sp"
            pos_hint: {"center_x": .5, "center_y": .5}
            theme_icon_color: "Custom"
            icon_color: 0, 0.8, 1, 1

        MDLabel:
            text: "STATUS: SECURE"
            halign: "center"
            pos_hint: {"center_y": .4}
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
'''

class LockScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class ShadowMonarchApp(MDApp):
    def build(self):
        # Setting a dark theme to match your style
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_string(KV)

if __name__ == '__main__':
    ShadowMonarchApp().run()
