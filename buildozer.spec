[app]

# (str) Title of your application
title = Shadow Monarch

# (str) Package name
package.name = shadowmonarch

# (str) Package domain (needed for android packaging)
package.domain = org.king

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
# ملاحظة: تأكد من تسمية ملف الخط cairo.ttf في المجلد وفي الكود
source.include_exts = py,png,jpg,jpeg,ttf,json

# (list) Application requirements
requirements = python3, kivy==2.3.0, kivymd, pillow, requests, urllib3, charset-normalizer, idna, openssl

# (str) Application version
version = 1.0

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, CAMERA

# (int) Target Android API
android.api = 33

# (int) Minimum API
android.minapi = 21

# (bool) Fullscreen
fullscreen = 1

# (str) Android NDK version
android.ndk = 25b

# (bool) Accept SDK license
android.accept_sdk_license = True

# (list) Android architectures
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

# (int) Log level (2 = error/info)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
