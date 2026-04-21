import sys
import traceback
from kivy.logger import Logger
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

# Enable detailed logging for debugging
Logger.setLevel('debug')

class TestApp(MDApp):
    def build(self):
        try:
            self.theme_cls.theme_style = "Dark"
            screen = MDScreen()
            screen.add_widget(
                MDLabel(
                    text="SYSTEM ACTIVE - NO IMAGES",
                    halign="center",
                    font_style="H3"
                )
            )
            Logger.info("TestApp", "App built successfully")
            return screen
        except Exception as e:
            Logger.error("TestApp", f"Error building app: {str(e)}")
            Logger.error("TestApp", traceback.format_exc())
            # Return minimal fallback UI
            fallback_screen = MDScreen()
            fallback_screen.add_widget(MDLabel(text=f"ERROR: {str(e)}"))
            return fallback_screen

if __name__ == '__main__':
    try:
        TestApp().run()
    except Exception as e:
        Logger.critical("TestApp", f"Critical error: {str(e)}")
        Logger.critical("TestApp", traceback.format_exc())
        sys.exit(1)
