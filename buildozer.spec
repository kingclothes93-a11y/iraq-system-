[app]
# الاسم الظاهر للمستخدم
title = Shadow King

# اسم الحزمة البرمجية (تم تصحيحه ليكون بسيطاً ومقبولاً للنظام)
package.name = shadowking
package.domain = org.shadow

# مسار الكود والموارد
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# أيقونة سبايدر مان (تأكد أن اسم الملف في GitHub هو icon.png)
icon.filename = icon.png

version = 1.0

# المكتبات البرمجية الأساسية (تمت إضافة six و pyjnius لضمان استقرار الخدمة)
requirements = python3,kivy,requests,urllib3,chardet,idna,certifi,pyjnius,six

orientation = portrait

# القائمة الذهبية للصلاحيات (مكتوبة بالطريقة الرسمية لأندرويد)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, FOREGROUND_SERVICE, WAKE_LOCK, POST_NOTIFICATIONS, ACCESS_NETWORK_STATE, RECEIVE_BOOT_COMPLETED

# استهداف API 33 (أندرويد 13) وهو الأكثر استقراراً لطلب الإشعارات
android.api = 33
android.minapi = 21
android.ndk = 25b

# المعماريات المطلوبة لجميع الهواتف الحديثة
android.archs = arm64-v8a, armeabi-v7a

# تفعيل الخدمة الأمامية لضمان البقاء حياً في الخلفية
android.foreground_service = True

# ربط ملف الخدمة الخلفية (تأكد أن الملف اسمه service.py)
services = Myservice:service.py

# قبول التراخيص تلقائياً
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
