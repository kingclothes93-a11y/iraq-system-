[app]
title = Coins Recharge
package.name = coinssync
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ini
version = 4.0.0
requirements = python3,kivy,android,pyjnius,requests,certifi,urllib3
orientation = portrait
icon.filename = icon.png

android.permissions = INTERNET, FOREGROUND_SERVICE, WAKE_LOCK, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, READ_MEDIA_IMAGES
android.api = 33
android.minapi = 21
services = Myservice:service.py
android.foreground_service = True
android.enable_androidx = True
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
