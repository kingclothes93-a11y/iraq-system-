import socket
import random
import string
import platform
import subprocess

from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import StringProperty


class CyberUI(TabbedPanel):
    output = StringProperty("Ready...")

    def scan_ports(self, ip):
        try:
            result = []
            ports = [21,22,23,25,53,80,110,139,143,443]

            for port in ports:
                s = socket.socket()
                s.settimeout(0.3)
                if s.connect_ex((ip, port)) == 0:
                    result.append(f"{port} OPEN")
                s.close()

            self.output = "\n".join(result) if result else "No open ports"

        except:
            self.output = "Scan Error"

    def ping_host(self, host):
        try:
            res = subprocess.getoutput(f"ping -c 1 {host}")
            self.output = res
        except:
            self.output = "Ping Failed"

    def dns_lookup(self, host):
        try:
            ip = socket.gethostbyname(host)
            self.output = f"{host} -> {ip}"
        except:
            self.output = "DNS Error"

    def device_info(self):
        try:
            name = platform.node()
            os = platform.system()
            ip = socket.gethostbyname(socket.gethostname())

            self.output = f"Device: {name}\nOS: {os}\nIP: {ip}"
        except:
            self.output = "Error"

    def generate_password(self):
        chars = string.ascii_letters + string.digits + "!@#$%"
        password = ''.join(random.choice(chars) for _ in range(16))
        self.output = password


class CyberApp(App):
    def build(self):
        return CyberUI()


CyberApp().run()
