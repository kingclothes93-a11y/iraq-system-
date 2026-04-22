[app]
title = Shadow Monarch
package.name = shadowmonarch
package.domain = org.kingclothes
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0
requirements = python3,kivy==2.3.0,urllib3
orientation = portrait
android.archs = arm64-v8a
android.allow_backup = False
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.bootstrap = sdl2
android.wakelock = False
p4a.branch = master
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/25.1.8937393

[buildozer]
log_level = 2
warn_on_root = 1
