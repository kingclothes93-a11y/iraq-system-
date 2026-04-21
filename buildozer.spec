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
source.include_exts = py,png,jpg,jpeg,json

# (str) Application version
version = 1.0.0

# (list) Application requirements - VERSIONS MUST BE COMPATIBLE
requirements = python3, kivy==2.2.1, kivymd==1.2.0, pillow, requests

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, ACCESS_NETWORK_STATE

# (int) Target Android API
android.api = 33

# (int) Minimum API
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (bool) Use private data storage
android.private_storage = True

# (bool) Accept SDK license
android.accept_sdk_license = True

# (str) Android entry point
android.entrypoint = main.py

# (list) The Android architectures
android.archs = arm64-v8a, armeabi-v7a

# (str) Android bootstrap
android.bootstrap = sdl2

# (bool) Auto backup feature
android.autobackup = False

# (str) Application icon and presplash
# android.icon = data/icon.png
# android.presplash = data/presplash.png

[buildozer]

# (int) Log level (2 = debug)
log_level = 2

# (int) Display warning if run as root
warn_on_root = 1
