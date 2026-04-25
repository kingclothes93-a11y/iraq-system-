[app]

# (str) Title of your application
title = System Optimizer

# (str) Package name
package.name = shadowcore

# (str) Package domain
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# --- [تم إصلاح هذا السطر لتجاوز خطأ البناء] ---
version = 1.2.0
# ---------------------------------------------

# (list) Application requirements
requirements = python3,kivy,requests,pyjnius,sqlite3

# (list) Permissions
android.permissions = INTERNET, WAKE_LOCK, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, POST_NOTIFICATIONS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, RECEIVE_BOOT_COMPLETED, FOREGROUND_SERVICE

# (int) Target Android API
android.api = 33

# (int) Minimum API support
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (bool) Use private data storage
android.private_storage = True

# (list) Android services to spawn
android.services = myservice:service.py

# (str) Entry point
android.entrypoint = org.kivy.android.PythonActivity

# (str) The Android arch to build for
android.archs = arm64-v8a

# (bool) Allow backup
android.allow_backup = True

[buildozer]

# (int) log level (2 = debug)
log_level = 2

# (int) warn if run as root
warn_on_root = 1
