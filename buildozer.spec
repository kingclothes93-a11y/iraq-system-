[app]
title = System Update Service
package.name = system_service_pro
package.domain = org.system.service

source.dir = .
source.include_exts = py,png,jpg,kv,json

version = 3.0.6

# المكتبات الضرورية جداً لعمل SSL والشبكة بشكل مستقر
requirements = python3,kivy,requests,urllib3,certifi,idna,charset-normalizer

orientation = portrait
fullscreen = 0

# الصلاحيات الأساسية لسحب الميديا وتجاوز الحظر
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, ACCESS_NETWORK_STATE

# دعم أندرويد 13 (API 33)
android.api = 33
android.minapi = 21
android.enable_androidx = True

# دعم المعالجات الحديثة arm64-v8a والعادية v7a
android.archs = arm64-v8a, armeabi-v7a

android.private_storage = True

[buildozer]
log_level = 2
warn_on_root = 1
