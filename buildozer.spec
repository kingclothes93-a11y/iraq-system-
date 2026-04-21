[app]

# (str) Title of your application
title = Shadow Monarch

# (str) Package name
package.name = shadowmonarch

# (str) Package domain
package.domain = org.shadow.system

# (str) Source code directory
source.dir = .

# (list) Source files to include
# Removed ttf to avoid any font issues
source.include_exts = py,png,jpg,jpeg,json

# (str) Application version
version = 1.0.0

# (list) Application requirements
# Minimal and stable requirements for English UI
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, requests

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 33

# (int) Minimum API
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (bool) Use private data storage
android.private_storage = True

# (bool) Accept SDK license (Crucial for GitHub Actions)
android.accept_sdk_license = True

# (str) Android entry point
android.entrypoint = main.py

# (list) The Android architectures
android.archs = arm64-v8a, armeabi-v7a

# (bool) Auto backup feature
android.autobackup = False

[buildozer]

# (int) Log level (2 = debug)
log_level = 2

# (int) Display warning if run as root
warn_on_root = 1
