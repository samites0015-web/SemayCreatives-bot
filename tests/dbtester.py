import sqlite3
import random
import string
from datetime import datetime

# Helper function to generate random strings
def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to create the database and insert data
def create_db_and_insert_data(admins_count, courses_count, payments_count, users_count):
    # Connect to SQLite database (it will create the file if it doesn't exist)
    conn = sqlite3.connect('tests/testmain.db')
    cursor = conn.cursor()

    # Create the 'admins' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            telegram_id INTEGER PRIMARY KEY
        )
    ''')

    # Create the 'courses' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL,
            refund_days INTEGER,
            poster_id TEXT,
            showreel_id TEXT,
            invite_link TEXT
        )
    ''')

    # Create the 'payments' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            tx_ref TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            price REAL NOT NULL,
            purchased_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create the 'users' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            language TEXT DEFAULT 'en'
        )
    ''')

    # Insert data into the 'admins' table
    for _ in range(admins_count):
        telegram_id = random.randint(1000000000, 9999999999)
        cursor.execute('''
            INSERT INTO admins (telegram_id) VALUES (?)
        ''', (telegram_id,))

    # Insert data into the 'courses' table
    for _ in range(courses_count):
        name = random_string(10)  # Random course name
        price = random.uniform(10, 500)  # Random price between 10 and 500
        refund_days = random.randint(0, 30)  # Random refund days between 0 and 30
        poster_id = random_string(10)  # Random poster ID
        showreel_id = random_string(10)  # Random showreel ID
        invite_link = f"https://example.com/{random_string(10)}"  # Random invite link

        cursor.execute('''
            INSERT INTO courses (name, price, refund_days, poster_id, showreel_id, invite_link) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, price, refund_days, poster_id, showreel_id, invite_link))

    # Insert data into the 'users' table
    for _ in range(users_count):
        language = random.choice(['en', 'es', 'fr', 'de', 'it'])  # Random language
        cursor.execute('''
            INSERT INTO users (language) VALUES (?)
        ''', (language,))

    # Insert data into the 'payments' table
    for _ in range(payments_count):
        tx_ref = random_string(15)  # Random transaction reference
        user_id = random.randint(1, users_count)  # Random user ID
        course_id = random.randint(1, courses_count)  # Random course ID
        price = random.uniform(10, 500)  # Random price between 10 and 500
        purchased_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp

        cursor.execute('''
            INSERT INTO payments (tx_ref, user_id, course_id, price, purchased_at) 
            VALUES (?, ?, ?, ?, ?)
        ''', (tx_ref, user_id, course_id, price, purchased_at))

    # Commit and close the connection
    conn.commit()
    conn.close()

    print(f"Database 'main.db' created and populated with:")
    print(f" - {admins_count} admins")
    print(f" - {courses_count} courses")
    print(f" - {payments_count} payments")
    print(f" - {users_count} users")

# Example usage: change the row numbers to test
admins_rows = 10
courses_rows = 100
payments_rows = 100000
users_rows = 500000

# Create the database and insert data
create_db_and_insert_data(admins_rows, courses_rows, payments_rows, users_rows)
