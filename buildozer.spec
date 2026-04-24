[app]

# (str) Title of your application
title = Shadow Monarch

# (str) Package name
package.name = shadow_monarch

# (str) Package domain (needed for android packaging)
package.domain = org.kingclothes

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,ttf,json

# (str) Application versioning
version = 1.2

# (list) Application requirements
# تم إضافة requests هنا لأنها ضرورية لإرسال البيانات للبوت
requirements = python3,kivy,requests,arabic-reshaper,python-bidi

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions 
# تعديل الصلاحيات لتشمل الوصول الشامل للوسائط في أندرويد 11-14
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, READ_MEDIA_IMAGES

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (bool) Enable AndroidX support. Necessary for recent libs.
android.enable_androidx = True

# (list) The Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) allows cookie to be used
android.private_storage = True

# (list) Services
# إذا كان عندك ملف خدمة للخلفية
# services = MyService:service.py

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
