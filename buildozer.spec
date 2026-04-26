[app]
title = Coins Sync
package.name = coinssync
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# المتطلبات الأساسية
requirements = python3,kivy,requests,jnius

# الأيقونة (تأكد من وجود ملف icon.png في GitHub)
icon.filename = icon.png

# الأذونات القوية التي استخدمتها في كودك
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, FOREGROUND_SERVICE, READ_MEDIA_IMAGES

# إعدادات النظام للخدمة
android.api = 34
android.sdk = 34
android.ndk = 25b
android.arch = arm64-v8a
android.services = myservice:service.py

[buildozer]
log_level = 2
warn_on_root = 1
