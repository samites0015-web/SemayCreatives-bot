import sqlite3

DB_PATH = "data/main.db"

def get_all_courses():
    """Return all courses as a dict keyed by course id."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT id, name, price, refund_days, poster_id, showreel_id, invite_link
        FROM courses
    """)
    courses = {
        row[0]: {
            "name": row[1],
            "price": row[2],
            "refund_days": row[3],
            "poster_id": row[4],
            "showreel_id": row[5],
            "invite_link": row[6]
        }
        for row in c.fetchall()
    }
    conn.close()
    return courses

def get_course(course_id):
    """Return a single course dict by id, or None if not found."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT id, name, price, refund_days, poster_id, showreel_id, invite_link
        FROM courses
        WHERE id=?
    """, (course_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "name": row[1],
            "price": row[2],
            "refund_days": row[3],
            "poster_id": row[4],
            "showreel_id": row[5],
            "invite_link": row[6]
        }
    return None