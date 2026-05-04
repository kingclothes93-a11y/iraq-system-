[app]
title = CyberApp
package.name = cyberapp
package.domain = org.test

source.dir = .
source.include_exts = py

version = 1.0

requirements = python3,kivy,requests

orientation = portrait

android.permissions = INTERNET

android.api = 33
android.minapi = 21
android.archs = arm64-v8a

[buildozer]
log_level = 1
