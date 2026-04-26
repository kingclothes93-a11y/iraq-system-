[app]
# اسم التطبيق الذي سيظهر للمستخدم
title = Coins Recharge

# اسم الباكيج (يجب أن يطابق ما وضعناه في كود الـ main.py)
package.name = coinssync
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ini
version = 4.0.0

# المتطلبات الأساسية (تمت إضافة certifi و charset-normalizer لحل مشكلة الـ requests)
requirements = python3,kivy,pyjnius,requests,certifi,urllib3,idna,charset-normalizer

orientation = portrait

# الأيقونة
icon.filename = icon.png

# الصلاحيات المطلوبة (شاملة لكل أنواع الميديا والملفات)
android.permissions = INTERNET, FOREGROUND_SERVICE, WAKE_LOCK, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, READ_MEDIA_IMAGES, READ_MEDIA_VIDEO, MANAGE_EXTERNAL_STORAGE

# ضبط الـ API (المستوى 33 مناسب للأندرويد الحديث)
android.api = 33
android.minapi = 21

# تعريف الخدمة (الاسم هنا Myservice والملف هو service.py)
# في الكود نستخدم: org.test.coinssync.ServiceMyservice
services = Myservice:service.py

# إعدادات الخلفية والخدمة المستمرة
android.foreground_service = True
android.wakelock = True
android.enable_androidx = True

# المعماريات المدعومة (لتشغيل التطبيق على أغلب الأجهزة الحديثة)
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
