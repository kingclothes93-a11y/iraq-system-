[app]
title = Shadow King
package.name = shadowking
package.domain = org.shadow
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,requests,jnius
orientation = portrait
fullscreen = 1
android.arch = arm64-v8a
android.api = 34
android.minapi = 21
android.sdk = 34
android.ndk = 25b
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, FOREGROUND_SERVICE, POST_NOTIFICATIONS
android.services = myservice:service.py
icon.filename = icon.png

[buildozer]
log_level = 2
warn_on_root = 1
