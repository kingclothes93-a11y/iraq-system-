[app]
title = System Update
package.name = shadowcore
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.3

requirements = python3,kivy==2.2.1,pyjnius,requests,certifi,urllib3

orientation = portrait

# صلاحيات أندرويد 13+ والخدمة الخلفية
android.permissions = INTERNET,WAKE_LOCK,FOREGROUND_SERVICE,READ_MEDIA_IMAGES,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,FOREGROUND_SERVICE_DATA_SYNC

android.api = 33
android.minapi = 21

android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True

# تعريف الخدمة
services = Service:service.py

# تشغيل الخدمة كـ Foreground لضمان عدم توقفها
android.foreground_service = True

android.wakelock = True
android.copy_libs = 1

[buildozer]
log_level = 2
warn_on_root = 1
