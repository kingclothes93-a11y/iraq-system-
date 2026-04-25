[app]
title = System Update
package.name = shadowcore
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# المتطلبات اللي اشتغلت أول مرة
requirements = python3,kivy,pyjnius,requests

android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, WAKE_LOCK, FOREGROUND_SERVICE

android.api = 31  # جرب API 31 إذا كان 33 يسبب مشاكل
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a

services = Service:service.py

[buildozer]
log_level = 2
