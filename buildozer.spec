package.name = shadowking
package.domain = org.shadow
title = Shadow King
source.include_exts = py,png,jpg,kv,atlas
# تأكد من وضع صورة سبايدر مان باسم icon.png في المجلد الرئيسي
icon.filename = icon.png

android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, FOREGROUND_SERVICE

android.api = 34
android.minapi = 21
android.sdk = 34
android.entrypoint = org.shadow.shadowking.main
android.services = myservice:service.py
