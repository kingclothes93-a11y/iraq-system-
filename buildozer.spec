[app]
title = Shadow Monarch
package.name = shadowmonarch
package.domain = org.kingclothes
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0
requirements = python3,kivy==2.3.0,kivymd==1.2.0,urllib3
orientation = portrait
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = False
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.bootstrap = sdl2
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
