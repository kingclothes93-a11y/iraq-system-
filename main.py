from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
import os
import socket
import requests
import random
import string

KV_FILE = os.path.join(os.path.dirname(__file__), "cyber.kv")
Builder.load_file(KV_FILE)


class LoginScreen(Screen):
    def check_password(self):
        if self.ids.pass_input.text == "20057":
            self.manager.current = "main"
        else:
            self.ids.pass_input.text = ""


class MainScreen(Screen):
    output = StringProperty("Ready...")

    def dns_lookup(self, host):
        try:
            ip = socket.gethostbyname(host)
            self.output = f"{host} -> {ip}"
        except:
            self.output = "DNS Error"

    def ip_info(self, ip):
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
            self.output = str(r)
        except:
            self.output = "No Internet / Error"

    def headers(self, url):
        try:
            r = requests.get(url, timeout=5)
            self.output = "\n".join([f"{k}: {v}" for k, v in r.headers.items()])
        except:
            self.output = "Request Failed"

    def password(self):
        chars = string.ascii_letters + string.digits
        self.output = ''.join(random.choice(chars) for _ in range(16))

    def device(self):
        try:
            name = socket.gethostname()
            ip = socket.gethostbyname(name)
            self.output = f"Device: {name}\nIP: {ip}"
        except:
            self.output = "Error"


class Manager(ScreenManager):
    pass


class CyberApp(App):
    def build(self):
        return Manager()


CyberApp().run()
