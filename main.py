from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout


# ===== Splash Screen =====
class SplashScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        bg = Image(
            source="bg_lock.jpg",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )

        title = MDLabel(
            text="SHADOW MONARCH",
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            theme_text_color="Custom",
            text_color=(0, 0.8, 1, 1),
            font_style="H4"
        )

        btn = MDRaisedButton(
            text="ENTER",
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            on_release=self.go_main
        )

        layout.add_widget(bg)
        layout.add_widget(title)
        layout.add_widget(btn)

        self.add_widget(layout)

    def go_main(self, *args):
        self.manager.current = "main"


# ===== Main Screen =====
class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        bg = Image(
            source="bg_main.jpg",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )

        text = MDLabel(
            text="Welcome to Shadow System",
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H5"
        )

        layout.add_widget(bg)
        layout.add_widget(text)

        self.add_widget(layout)


# ===== App =====
class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"

        sm = MDScreenManager()
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(MainScreen(name="main"))

        sm.current = "splash"
        return sm


if __name__ == "__main__":
    MainApp().run()
