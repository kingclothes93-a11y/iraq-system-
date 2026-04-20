[app]
# (str) Title of your application
title = Shadow Monarch

# (str) Package name
package.name = shadowmonarch

# (str) Package domain (needed for android packaging)
package.domain = org.king

# (str) Source code where the main.py live
source.dir = .

# (str) Application version (هذا السطر اللي كان ناقص)
version = 1.0

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
requirements = python3, kivy==2.3.0, kivymd, pillow, requests, urllib3, charset-normalizer, idna

# (str) Supported orientations
orientation = portrait

# (bool) Fullscreen
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 33

# (int) Minimum API
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (bool) Accept SDK license
android.accept_sdk_license = True

# (list) Android architectures
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
