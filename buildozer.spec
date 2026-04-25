[app]

# (str) Title of your application
title = System Update Service

# (str) Package name
package.name = system_update_service

# (str) Package domain (needed for android packaging)
package.domain = org.system.service

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf,json

# (str) Application versioning
version = 3.0.4

# (list) Application requirements
# أضفنا certifi و urllib3 لضمان عمل الـ HTTPS مع تليجرام
requirements = python3,kivy,requests,urllib3,certifi,idna,charset-normalizer

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# استخدمنا صلاحيات مستقرة لتجنب الانهيار في أندرويد 11+
android.permissions = INTERNET, ACCESS_NETWORK_STATE, READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (list) Architecture to build for
# دعم المعالجات الحديثة arm64 والمعالجات العادية v7a
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables AndroidX, which is required for many modern libraries
android.enable_androidx = True

# (str) The Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpython.so
android.copy_libs = 1

# (str) Bootstrap to use for android content
p4a.branch = master

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = no, 1 = yes)
warn_on_root = 1
