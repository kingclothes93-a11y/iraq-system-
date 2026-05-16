[app]

title = Iraq System
package.name = iraqsystem
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

# Android config
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

android.accept_sdk_license = True

android.permissions = INTERNET

android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True
android.release_artifact = apk

log_level = 2
warn_on_root = 1
