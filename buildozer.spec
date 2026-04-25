[app]
# اسم التطبيق الذي سيظهر على الشاشة
title = ShadowCore System

# اسم الحزمة (يجب أن يكون فريداً)
package.name = shadowcore
package.domain = org.shadowcore

# مجلد الكود المصدري
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,txt
source.exclude_exts = spec

# الإصدار
version = 2.0.0

# المكتبات المطلوبة (تم إضافة jnius و android لضمان الصلاحيات)
requirements = python3,kivy,requests,urllib3,chardet,certifi,idna,pyjnius,android

# تثبيت اتجاه الشاشة بالطول (Portrait) كما طلبت
orientation = portrait

# تعطيل وضع الشاشة الكاملة لرؤية شريط الإشعارات
fullscreen = 0

# استهداف أحدث واجهة برمجية لأندرويد
android.api = 33
android.minapi = 21
android.sdk = 33

# الصلاحيات (أهم جزء للوصول للصور والخدمة الخلفية)
android.permissions = INTERNET, FOREGROUND_SERVICE, WAKE_LOCK, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, READ_MEDIA_IMAGES, READ_MEDIA_VIDEO

# تعريف الخدمة الخلفية (يجب أن يطابق الاسم الموجود في main.py)
services = Myservice:service.py

# إعدادات الخدمة في الأندرويد
android.foreground_service = True
android.wakelock = True

# دعم المعالجات الحديثة والقديمة
android.archs = arm64-v8a, armeabi-v7a

# قبول التراخيص تلقائياً عند البناء
android.accept_sdk_license = True

[buildozer]
# مستوى سجل الأخطاء (2 ليعطيك تفاصيل في حال فشل البناء)
log_level = 2
warn_on_root = 1
