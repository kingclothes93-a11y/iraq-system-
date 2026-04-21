[app]

title = Shadow Monarch
package.name = shadowmonarch
package.domain = org.king

source.dir = .

# مهم حتى يدخل الخط والصور
source.include_exts = py,png,jpg,jpeg,ttf,json,kv

# نسخ مستقرة ومجربة
requirements = python3==3.8.18,kivy==2.1.0,kivymd==1.1.1,requests

version = 1.0
orientation = portrait

android.permissions = INTERNET,CAMERA,READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21

fullscreen = 1

android.ndk = 25b
android.accept_sdk_license = True

android.archs = arm64-v8a, armeabi-v7a


[buildozer]

log_level = 2
warn_on_root = 1
