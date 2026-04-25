[app]

# (str) Title of your application
title = System Update Service

# (str) Package name
package.name = system_update_service

# (str) Package domain (needed for android packaging)
package.domain = org.shadowcore

# (str) Source code where the main.py is located
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.68

# (list) Application requirements
# IMPORTANT: certifi and idna are added for secure SSL connection
requirements = python3,kivy,requests,certifi,idna,openssl,urllib3

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# UPDATED for Android 13+ (Images and Video)
android.permissions = INTERNET, READ_MEDIA_IMAGES, READ_MEDIA_VIDEO, FOREGROUND_SERVICE

# (int) Target Android API, should be as high as possible.
# API 34 is for Android 14
android.api = 34

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 34

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (list) Architecture to build for (keep only arm64-v8a for speed or add armeabi-v7a)
android.archs = arm64-v8a

# (bool) Allow backup
android.allow_backup = True

# (str) The format used to package the app for release mode (aab or apk)
android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk or aab)
android.debug_artifact = apk

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1
