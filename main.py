from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        self.add_widget(Label(text="Iraq System 🇮🇶"))
        self.add_widget(Label(text="App is working successfully"))

class IraqApp(App):
    def build(self):
        return MainLayout()

if __name__ == "__main__":
    IraqApp().run()
