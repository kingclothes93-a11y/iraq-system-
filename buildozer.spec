[app]
title = Shadow Monarch
package.name = shadowmonarch
package.domain = org.kingclothes
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ttf
version = 1.0
requirements = python3,kivy==2.3.0,urllib3
orientation = portrait
android.archs = arm64-v8a
android.allow_backup = False
android.permissions = INTERNET
android.api = 34
android.minapi = 21
android.ndk = 25b
android.build_tools_version = 34.0.0
android.bootstrap = sdl2
android.wakelock = False
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
