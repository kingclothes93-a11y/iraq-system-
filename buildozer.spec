[app]
title = Shadow Monarch
package.name = shadowmonarch
package.domain = org.king
source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,json
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, requests
version = 1.0
orientation = portrait
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, CAMERA
android.api = 33
android.minapi = 21
fullscreen = 1
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
