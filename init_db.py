import sqlite3
import os

os.makedirs("data", exist_ok=True)
conn = sqlite3.connect("data/main.db")
c = conn.cursor()

# Admins table: only telegram_id
c.execute("""
CREATE TABLE IF NOT EXISTS admins (
    telegram_id INTEGER PRIMARY KEY
)
""")

# Courses table
c.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price REAL,
    refund_days INTEGER,
    poster_id TEXT,
    showreel_id TEXT
)
""")

# Payments table
c.execute("""
CREATE TABLE IF NOT EXISTS payments (
    tx_ref TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    price REAL NOT NULL,
    purchased_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Users table for language preference
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    language TEXT DEFAULT 'en'
)
""")

# Demo admin
c.execute("""
INSERT OR IGNORE INTO admins (telegram_id)
VALUES (?)
""", (123456789,))

# Demo courses
demo_courses = [
    (
        1,
        "Video Editing",
        200.0,
        2,
        "AgACAgQAAyEFAASWYGX-AANTaLrpQmS1frSSElYNBK8-T2_CGM4AArTRMRtFrtFRam2q7lWKGYkBAAMCAAN5AAM2BA",
        "BAACAgQAAyEFAASWYGX-AANPaLrSwz4SounRBKPV7kxNu6ho-CUAAg0fAAJFrtFRYrD03GLWLXk2BA",
    )
]
c.executemany("""
INSERT OR REPLACE INTO courses (id, name, price, refund_days, poster_id, showreel_id)
VALUES (?, ?, ?, ?, ?, ?)
""", demo_courses)

# Demo payment
c.execute("""
INSERT OR IGNORE INTO payments (tx_ref, user_id, course_id, price)
VALUES (?, ?, ?, ?)
""", ("demo_tx_001", 123456789, 1, 300.0))

conn.commit()
conn.close()
print("Database and tables created successfully as data/main.db with demo data.")