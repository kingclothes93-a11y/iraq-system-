[app]
title = System Update
package.name = shadowcore
package.domain = org.test
source.dir = .
version = 2.1
requirements = python3,kivy,pyjnius,requests,certifi
orientation = portrait

# الأذونات المطلوبة فقط
android.permissions = INTERNET,FOREGROUND_SERVICE,WAKE_LOCK,READ_MEDIA_IMAGES

android.api = 33
android.minapi = 21

services = Myservice:service.py

android.foreground_service = True
android.wakelock = True

[buildozer]
log_level = 2
