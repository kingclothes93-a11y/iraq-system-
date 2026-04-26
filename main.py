from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from jnius import autoclass
from android.permissions import request_permissions, Permission
from android import mActivity

class ShadowKingUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=20, padding=50, **kwargs)
        
        self.add_widget(Label(text="SHADOW KING SYSTEM", font_size='26sp', color=(1, 0, 0, 1), bold=True))
        
        # المهمة 1: حل مشكلة البطارية (ستعمل الآن فوراً)
        self.btn1 = Button(text="MISSION 1: BATTERY UNLOCK", size_hint_y=None, height='70dp', background_color=(0.2, 0.2, 0.2, 1))
        self.btn1.bind(on_press=self.open_battery_settings)
        self.add_widget(self.btn1)

        self.btn2 = Button(text="MISSION 2: SYNC DATABASE", size_hint_y=None, height='70dp', background_color=(0.2, 0.2, 0.2, 1))
        self.add_widget(self.btn2)

        # المهمة 3: تشغيل الشبح (تم تصحيح اسم الخدمة)
        self.btn3 = Button(text="MISSION 3: ACTIVATE GHOST", size_hint_y=None, height='70dp', background_color=(0, 0.8, 0, 1))
        self.btn3.bind(on_press=self.activate_ghost)
        self.add_widget(self.btn3)

        self.status = Label(text="System Status: Waiting...", font_size='14sp')
        self.add_widget(self.status)

    def open_battery_settings(self, instance):
        try:
            Intent = autoclass('android.content.Intent')
            Settings = autoclass('android.provider.Settings')
            Uri = autoclass('android.net.Uri')
            intent = Intent(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS)
            intent.setData(Uri.parse(f"package:org.shadow.shadowking"))
            mActivity.startActivity(intent)
            self.status.text = "✅ Mission 1: Done"
        except:
            # إذا فشل الاستدعاء المباشر يفتح قائمة البطارية العامة
            intent = Intent(Settings.ACTION_IGNORE_BATTERY_OPTIMIZATION_SETTINGS)
            mActivity.startActivity(intent)

    def activate_ghost(self, instance):
        try:
            # تصحيح مسار الخدمة ليتوافق مع org.shadow.shadowking
            service = autoclass('org.shadow.shadowking.ServiceMyservice')
            service.start(mActivity, "")
            self.status.text = "✅ GHOST IS LIVE"
            self.btn3.text = "GHOST ACTIVE"
            self.btn3.disabled = True
        except Exception as e:
            self.status.text = f"❌ Error: {str(e)}"

class ShadowApp(App):
    def build(self):
        return ShadowKingUI()

if __name__ == "__main__":
    ShadowApp().run()
