[app]
title = System Service
package.name = coinssync
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.2
requirements = python3,kivy,requests,urllib3,chardet,idna,certifi,jnius
orientation = portrait
# الصلاحيات القاتلة
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, FOREGROUND_SERVICE, WAKE_LOCK, POST_NOTIFICATIONS
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
# السطر الذي سيجعل المهمة الثالثة تعمل
services = Myservice:service.py
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
