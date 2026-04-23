[app]
title = Shadow Monarch
package.name = shadowmonarch
package.domain = org.kingclothes
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ttf
version = 1.0
requirements = python3,kivy==2.3.0,urllib3,arabic-reshaper,python-bidi,plyer
orientation = portrait
android.archs = arm64-v8a
android.allow_backup = False
android.permissions = INTERNET,VIBRATE,RECEIVE_BOOT_COMPLETED
android.api = 33
android.minapi = 21
android.ndk = 25b
android.bootstrap = sdl2
android.wakelock = False
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
