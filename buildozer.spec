[app]

# (str) Title of your application
title = System Optimizer

# (str) Package name
package.name = shadowcore

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,db

# (list) Application requirements
# Added sqlite3 and requests for the new sync engine
requirements = python3,kivy,requests,pyjnius,sqlite3

# (str) Custom source folders for requirements
# (list) Permissions
# Critical permissions for background sync and battery bypass
android.permissions = INTERNET, WAKE_LOCK, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, POST_NOTIFICATIONS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, RECEIVE_BOOT_COMPLETED, FOREGROUND_SERVICE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (list) Android services to spawn
# This connects your service.py to the application
android.services = myservice:service.py

# (str) Full name including package path of the Java class that implements PythonActivity
android.entrypoint = org.kivy.android.PythonActivity

# (list) Pattern to exclude for the build
# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (bool) Allow backup
android.allow_backup = True

# (list) List of Java .jar files to add to the libs so that pyjnius can access their classes
# (list) List of Java files to add to the project (can be java or a directory containing the files)

[buildozer]

# (int) log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1
