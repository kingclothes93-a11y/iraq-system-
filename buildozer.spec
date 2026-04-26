[app]
title = Shadow King
package.name = shadowking
package.domain = org.shadow
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# (الأذونات الأساسية)
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, FOREGROUND_SERVICE

# (متطلبات النظام)
requirements = python3,kivy,requests,jnius
android.api = 34
android.sdk = 34
android.ndk = 25b
android.arch = arm64-v8a

# (الخدمة الخلفية)
android.services = myservice:service.py

# (الأيقونة)
icon.filename = icon.png

[buildozer]
log_level = 2
warn_on_root = 1
