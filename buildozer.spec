[app]
title = ShadowCore System
package.name = coinssync
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.1
requirements = python3,kivy,requests,urllib3,chardet,idna,certifi,jnius
orientation = portrait
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, FOREGROUND_SERVICE, WAKE_LOCK, POST_NOTIFICATIONS
android.api = 33
android.minapi = 21
android.ndk = 25b
android.private_storage = True
android.archs = arm64-v8a, armeabi-v7a
services = Myservice:service.py
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
