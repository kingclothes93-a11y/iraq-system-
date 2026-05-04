from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty

import socket, random, string, platform, subprocess, requests
from concurrent.futures import ThreadPoolExecutor

Builder.load_file("cyber.kv")


class LoginScreen(Screen):
    def check_password(self):
        if self.ids.pass_input.text == "20057":
            self.manager.current = "main"
        else:
            self.ids.pass_input.text = ""


class MainScreen(Screen):
    output = StringProperty("Ready...")

    # 🔍 Port Scanner
    def scan_ports(self, ip):
        ports = [21,22,23,25,53,80,110,139,143,443,445,8080]
        open_ports = []

        def check(p):
            try:
                s = socket.socket()
                s.settimeout(0.3)
                if s.connect_ex((ip, p)) == 0:
                    open_ports.append(p)
                s.close()
            except:
                pass

        with ThreadPoolExecutor(max_workers=30) as ex:
            ex.map(check, ports)

        self.output = "Open Ports:\n" + str(open_ports) if open_ports else "No open ports"

    # 📡 Network Scan
    def network_scan(self):
        base = socket.gethostbyname(socket.gethostname()).rsplit('.',1)[0]
        active = []

        def ping(ip):
            res = subprocess.getoutput(f"ping -c 1 {ip}")
            if "ttl" in res.lower():
                active.append(ip)

        with ThreadPoolExecutor(max_workers=40) as ex:
            ex.map(ping, [f"{base}.{i}" for i in range(1,50)])

        self.output = "\n".join(active) if active else "No devices"

    # 🌍 DNS
    def dns_lookup(self, host):
        try:
            self.output = socket.gethostbyname(host)
        except:
            self.output = "DNS Error"

    # 📡 Ping
    def ping_host(self, host):
        self.output = subprocess.getoutput(f"ping -c 1 {host}")

    # 🌐 IP Info
    def ip_info(self, ip):
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}").json()
            self.output = str(r)
        except:
            self.output = "Error"

    # 🌐 Headers
    def headers(self, url):
        try:
            r = requests.get(url)
            self.output = "\n".join([f"{k}: {v}" for k,v in r.headers.items()])
        except:
            self.output = "Error"

    # 🛡️ Security Check
    def security(self, url):
        try:
            r = requests.get(url)
            h = r.headers
            checks = ["Content-Security-Policy","X-Frame-Options","Strict-Transport-Security"]
            result = []
            for c in checks:
                result.append(f"{c}: {'OK' if c in h else 'Missing'}")
            self.output = "\n".join(result)
        except:
            self.output = "Error"

    # 🧠 CVE
    def cve(self, key):
        try:
            r = requests.get(f"https://cve.circl.lu/api/search/{key}").json()
            data = r.get("data", [])[:3]
            self.output = "\n\n".join([d["id"] + "\n" + d["summary"] for d in data])
        except:
            self.output = "Error"

    # 🔐 Password
    def password(self):
        chars = string.ascii_letters + string.digits
        self.output = ''.join(random.choice(chars) for _ in range(16))

    # 💾 Save
    def save(self):
        try:
            with open("/storage/emulated/0/cyber_report.txt","w") as f:
                f.write(self.output)
            self.output = "Saved"
        except:
            self.output = "Save error"

    # 📶 Device
    def device(self):
        self.output = f"{platform.system()} | {socket.gethostname()}"


class Manager(ScreenManager):
    pass


class CyberApp(App):
    def build(self):
        return Manager()


CyberApp().run()
