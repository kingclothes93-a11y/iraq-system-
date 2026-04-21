[app]

# (str) Title of your application
title = Shadow Monarch

# (str) Package name
package.name = shadowmonarch

# (str) Package domain (needed for android packaging)
package.domain = org.shadow.system

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
# تم التأكد من تضمين ttf و json لضمان عمل الخط وحفظ الرسائل
source.include_exts = py,png,jpg,kv,atlas,ttf,json

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
# تم تحديث الإصدارات لضمان التوافق مع أندرويد 33 ومنع الانهيار
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, arabic-reshaper, python-bidi, requests, urllib3

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, CAMERA

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage
android.private_storage = True

# (bool) Accept SDK license (مهمة جداً لتجاوز خطأ الـ SDK السابق)
android.accept_sdk_license = True

# (str) Android entry point
android.entrypoint = main.py

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature
android.autobackup = False

[buildozer]

# (int) Log level (2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
