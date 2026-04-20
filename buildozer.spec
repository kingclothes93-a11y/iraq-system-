[app]
title = KingSystem
package.name = kingsystem
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

requirements = python3==3.8.18,kivy==2.1.0,requests

orientation = portrait

android.api = 33
android.minapi = 21
android.ndk = 25b

android.archs = arm64-v8a

android.permissions = INTERNET

android.accept_sdk_license = True
