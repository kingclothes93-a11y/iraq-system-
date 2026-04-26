from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from jnius import autoclass
from android.permissions import request_permissions, Permission

class ShadowKingUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=20, padding=50, **kwargs)
        
        self.add_widget(Label(text="SHADOW KING SYSTEM", font_size='26sp', color=(1, 0, 0, 1), bold=True))
        
        # المهمة 1: الصلاحيات
        self.btn1 = Button(text="MISSION 1: GRANT POWER", size_hint_y=None, height='70dp', background_color=(0.2, 0.2, 0.2, 1))
        self.btn1.bind(on_press=self.ask_permissions)
        self.add_widget(self.btn1)

        # المهمة 2: المزامنة (شكلية حالياً)
        self.btn2 = Button(text="MISSION 2: SYNC DATABASE", size_hint_y=None, height='70dp', background_color=(0.2, 0.2, 0.2, 1))
        self.add_widget(self.btn2)

        # المهمة 3: تشغيل الشبح
        self.btn3 = Button(text="MISSION 3: ACTIVATE GHOST", size_hint_y=None, height='70dp', background_color=(0, 0.8, 0, 1))
        self.btn3.bind(on_press=self.activate_ghost)
        self.add_widget(self.btn3)

        self.status = Label(text="System Status: Dormant", font_size='14sp', color=(0.8, 0.8, 0.8, 1))
        self.add_widget(self.status)

    def ask_permissions(self, instance):
        request_permissions([
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.POST_NOTIFICATIONS
        ])
        self.btn1.text = "✅ POWER GRANTED"

    def activate_ghost(self, instance):
        try:
            # الربط الدقيق مع الحزمة والخدمة المعرفة في buildozer.spec
            from android import mActivity
            service = autoclass('org.shadow.shadowking.ServiceMyservice')
            service.start(mActivity, "")
            self.status.text = "✅ GHOST IS LIVE IN BACKGROUND"
            self.btn3.text = "GHOST ACTIVE"
            self.btn3.disabled = True
        except Exception as e:
            self.status.text = f"❌ Error: {str(e)}"

class ShadowApp(App):
    def build(self):
        return ShadowKingUI()

if __name__ == "__main__":
    ShadowApp().run()
