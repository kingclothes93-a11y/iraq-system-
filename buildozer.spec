[app]
title = CyberToolkitPRO
package.name = cybertoolkit
package.domain = org.cyber

source.dir = .
source.include_exts = py,kv

version = 3.0

requirements = python3,kivy,requests

orientation = portrait

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21

[buildozer]
log_level = 2
