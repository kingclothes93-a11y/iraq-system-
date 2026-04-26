[app]
title = Photo Backup
package.name = shadowcore
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy,pyjnius,requests,certifi,urllib3

orientation = portrait

# الأذونات المهمة فقط (مضمونة)
android.permissions = INTERNET,FOREGROUND_SERVICE,WAKE_LOCK,READ_MEDIA_IMAGES

android.api = 33
android.minapi = 21

# تعريف الخدمة (مهم جدًا)
services = MyService:service.py

# تشغيل بالخلفية
android.foreground_service = True
android.wakelock = True

# تحسين التوافق
android.enable_androidx = True
android.copy_libs = 1

[buildozer]
log_level = 2
warn_on_root = 1
