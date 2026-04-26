[app]
# (str) Title of your application
title = ShadowCore System

# (str) Package name
package.name = coinssync

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application version
version = 1.1

# (list) Application requirements
# الأساسيات مع المكتبات المطلوبة للإنترنت والتعامل مع النظام
requirements = python3,kivy,requests,urllib3,chardet,idna,certifi,jnius

# (str) Supported orientation
orientation = portrait

# (list) Permissions
# تم إضافة POST_NOTIFICATIONS لأندرويد 13+ و FOREGROUND_SERVICE للخلفية
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, FOREGROUND_SERVICE, WAKE_LOCK, POST_NOTIFICATIONS

# (int) Target Android API, should be as high as possible.
# API 33 هو المطلوب لأندرويد 13 وطلب إذن الإشعارات
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use private storage for your app
android.private_storage = True

# (str) Android entry point, default is ok for Kivy
android.entrypoint = org.kivy.android.PythonActivity

# (list) Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (list) Services to declare
# هذا السطر هو المسؤول عن تشغيل الـ service.py في الخلفية
services = Myservice:service.py

# (bool) Indicated if the app should be signed for releasing
android.release = False

# (bool) Skip byte compile for .py files
android.skip_byte_compile = False

# (bool) Allow the app to be installed on external storage
android.allow_backup = True

# (bool) Accept SDK license
android.accept_sdk_license = True

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
