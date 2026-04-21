[app]

# (str) اسم التطبيق الذي سيظهر على الهاتف
title = Shadow Monarch

# (str) اسم الحزمة (يفضل أن يكون فريداً وبدون مسافات)
package.name = shadowmonarch

# (str) النطاق (Domain) الخاص بالحزمة
package.domain = org.king

# (str) المجلد الذي يحتوي على main.py
source.dir = .

# (list) الامتدادات التي سيتم تضمينها داخل التطبيق
# تأكد من وجود ttf لكي يقرأ ملف الخط cairo.ttf
source.include_exts = py,png,jpg,jpeg,ttf,json

# (list) المكتبات المطلوبة للتشغيل (مهمة جداً لعدم الانهيار)
requirements = python3, kivy==2.3.0, kivymd, pillow, requests, urllib3, charset-normalizer, idna, openssl

# (str) إصدار التطبيق
version = 1.0

# (str) وضع الشاشة (طولي)
orientation = portrait

# (list) الصلاحيات المطلوبة (تم إضافة الكاميرا والملفات كما في الكود)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, CAMERA

# (int) استهداف أحدث إصدار أندرويد مستقر
android.api = 33

# (int) أقل إصدار أندرويد يعمل عليه التطبيق
android.minapi = 21

# (bool) شاشة كاملة
fullscreen = 1

# (str) إصدار الـ NDK المتوافق
android.ndk = 25b

# (bool) قبول رخص الـ SDK تلقائياً
android.accept_sdk_license = True

# (list) المعماريات المدعومة للهواتف الحديثة والقديمة
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

# (int) مستوى السجل (2 لإظهار الأخطاء والمعلومات المهمة)
log_level = 2

# (int) عرض تحذير إذا تم التشغيل كجذر
warn_on_root = 1
