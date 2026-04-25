[app]
# (str) العنوان التمويهي
title = System Update Service

# (str) اسم الحزمة (يفضل تغييره قليلاً عن النسخة السابقة لتجنب تضارب التثبيت)
package.name = sys_v3_core
package.domain = org.system.service

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
version = 3.0

# (list) المكتبات المطلوبة - أضفت certifi و urllib3 لضمان عدم انهيار الاتصال المشفر
requirements = python3,kivy,requests,urllib3,certifi,chardet,idna,arabic-reshaper,python-bidi

orientation = portrait
fullscreen = 0

# (list) الصلاحيات - مرتبة بشكل يضمن الوصول الكامل
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE, ACCESS_FINE_LOCATION, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, POST_NOTIFICATIONS, FOREGROUND_SERVICE

# (int) استهداف أحدث API
android.api = 34
android.minapi = 21

# (bool) دعم أندرويد الحديث
android.enable_androidx = True

# (list) معالجات الأجهزة (arm64 مهم جداً للأجهزة الحديثة)
android.archs = arm64-v8a, armeabi-v7a

# (bool) السماح بالوصول للبيانات
android.private_storage = True

# (list) تفعيل الخدمات الخلفية إذا كنت تريد تشغيل الكود كـ Service
# services = MyCoreService:service.py

[buildozer]
log_level = 2
warn_on_root = 1
