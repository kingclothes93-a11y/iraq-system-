from kivy.app import App
from kivy.uix.label import Label

class IraqApp(App):
    def build(self):
        return Label(text="Iraq System 🇮🇶")

if __name__ == "__main__":
    IraqApp().run()
