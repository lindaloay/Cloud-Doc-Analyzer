import sqlite3

conn = sqlite3.connect('files.db')  # تأكد أن هذا نفس اسم قاعدة البيانات في مشروعك
c = conn.cursor()

try:
    c.execute("ALTER TABLE files ADD COLUMN title TEXT")
    print("✅ تم إضافة العمود 'title' بنجاح.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("ℹ️ العمود 'title' موجود مسبقًا.")
    else:
        print("❌ حدث خطأ:", e)

conn.commit()
conn.close()
