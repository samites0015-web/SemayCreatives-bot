import sqlite3
import pygsheets
import shutil
import time
import os

# -------------------------------
# CONFIG
# -------------------------------
DB_PATH = "data/main.db"
TEMP_DB = "data/__payments_temp__.db"
SERVICE_JSON = "data/service_account.json"
SHEET_ID = "1aUFO2CA6kDjJPTDTW6zSRrADzlW5KjAFaEkvR8IcPg0"
# -------------------------------

# Make sure files exist
if not os.path.exists(DB_PATH):
    raise FileNotFoundError(f"Database file not found: {DB_PATH}")
if not os.path.exists(SERVICE_JSON):
    raise FileNotFoundError(f"Service account JSON not found: {SERVICE_JSON}")

# Connect to Google Sheets
gc = pygsheets.authorize(service_file=SERVICE_JSON)
sh = gc.open_by_key(SHEET_ID)
wks = sh.sheet1

# Upload payments function
def upload_payments():
    try:
        shutil.copy2(DB_PATH, TEMP_DB)
        conn = sqlite3.connect(TEMP_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM payments")
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        data.insert(0, columns)
        conn.close()
        wks.clear()
        wks.update_values('A1', data)
        os.remove(TEMP_DB)
        print(f"[{time.strftime('%H:%M:%S')}] Payments table uploaded successfully!")
        return True
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Error uploading payments table:", e)
        return False

# Run once when executed directly
if __name__ == "__main__":
    print("Starting Google Sheets upload script...")
    print("Uploading all payments to Google Sheets...")
    success = upload_payments()
    if success:
        print("Upload completed successfully!")
    else:
        print("Upload failed. Check the error messages above.")
    print("Script execution completed.")
