
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
source.include_exts = py,png,jpg,kv,atlas,ttf

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
# هذه المكتبات هي الأهم لدعم اللغة العربية والصور
requirements = python3,kivy==2.2.1,kivymd==1.1.1,arabic-reshaper,python-bidi,pillow

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage
android.private_storage = True

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
