[app]

# (str) Title of your application
title = Shadow Monarch

# (str) Package name
package.name = shadow_monarch

# (str) Package domain (needed for android packaging)
package.domain = org.kingclothes

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf,json

# (str) Application versioning (method 1)
version = 1.1

# (list) Application requirements
# ملاحظة: تم إضافة مكتبات التعريب هنا (arabic-reshaper و python-bidi)
requirements = python3,kivy,arabic-reshaper,python-bidi

# (str) Custom source folders for requirements
# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/bg_main.jpg

# (str) Icon of the application
# icon.filename = %(source.dir)s/icon.png

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 33

# (str) Android NDK version to use
#android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False), default is True
android.private_storage = True

# (str) Android entry point, default is to use start.py
#android.entrypoint = main.py

# (list) List of Java .jar files to add to the libs dir
#android.add_jars = foo.jar,bar.jar,path/to/baz.jar

# (list) List of Java files to add to the android project (for custom GLES code)
#android.add_src = 

# (list) Android AAR archives to add
#android.add_aars =

# (list) Gradle dependencies
#android.gradle_dependencies =

# (bool) Enable AndroidX support. Necessary for recent libs.
android.enable_androidx = True

# (list) whitelist
#android.whitelist =

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) allows cookie to be used
#android.copy_libs = 1

# (str) logcat filter to use
#android.logcat_filter = *:S python:D

# (str) Android logcat filters to use when printing the log
#android.logcat_filters = MyKey:D

# (bool) copy library to build dir
#android.copy_libs = 1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1

