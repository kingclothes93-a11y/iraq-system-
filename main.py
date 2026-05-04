from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import socket
import requests
import random
import string

class CyberApp(App):

    def build(self):
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.input = TextInput(hint_text="Enter domain or IP")
        self.output = TextInput(readonly=True)

        btn1 = Button(text="DNS Lookup")
        btn2 = Button(text="IP Info")
        btn3 = Button(text="Generate Password")

        btn1.bind(on_press=self.dns)
        btn2.bind(on_press=self.ipinfo)
        btn3.bind(on_press=self.password)

        self.layout.add_widget(self.input)
        self.layout.add_widget(btn1)
        self.layout.add_widget(btn2)
        self.layout.add_widget(btn3)
        self.layout.add_widget(self.output)

        return self.layout

    def dns(self, instance):
        try:
            ip = socket.gethostbyname(self.input.text)
            self.output.text = ip
        except:
            self.output.text = "DNS Error"

    def ipinfo(self, instance):
        try:
            r = requests.get(f"http://ip-api.com/json/{self.input.text}", timeout=5).json()
            self.output.text = str(r)
        except:
            self.output.text = "Error"

    def password(self, instance):
        chars = string.ascii_letters + string.digits
        self.output.text = ''.join(random.choice(chars) for _ in range(16))


CyberApp().run()
