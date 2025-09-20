import sqlite3
import pygsheets
import os
from datetime import datetime

# -------------------------------
# CONFIG
# -------------------------------
DB_PATH = "data/main.db"
SERVICE_JSON = "data/service_account.json"
SHEET_ID = "1aUFO2CA6kDjJPTDTW6zSRrADzlW5KjAFaEkvR8IcPg0"

# Initialize Google Sheets connection
def get_google_sheets_connection():
    """Get Google Sheets connection"""
    try:
        if not os.path.exists(SERVICE_JSON):
            raise FileNotFoundError(f"Service account JSON not found: {SERVICE_JSON}")
        
        gc = pygsheets.authorize(service_file=SERVICE_JSON)
        sh = gc.open_by_key(SHEET_ID)
        wks = sh.sheet1
        return wks
    except Exception as e:
        print(f"Error connecting to Google Sheets: {e}")
        return None

def clean_empty_rows(wks):
    """Remove empty rows from the sheet"""
    try:
        current_data = wks.get_all_values()
        # Filter out completely empty rows
        non_empty_rows = [row for row in current_data if any(cell.strip() for cell in row)]
        print(f"🧹 Cleaned {len(current_data) - len(non_empty_rows)} empty rows")
        return non_empty_rows
    except Exception as e:
        print(f"Error cleaning empty rows: {e}")
        return current_data

def add_payment_to_sheets(payment_data):
    """
    Add a single payment record to Google Sheets immediately
    payment_data should be a dict with: tx_ref, user_id, course_id, price, timestamp
    """
    try:
        wks = get_google_sheets_connection()
        if not wks:
            return False
        
        # Get current data and clean empty rows
        current_data = wks.get_all_values()
        cleaned_data = clean_empty_rows(wks)
        
        # If sheet is empty or only has headers, add headers
        if not cleaned_data or len(cleaned_data) == 0:
            headers = ['tx_ref', 'user_id', 'course_id', 'price', 'timestamp', 'payment_method']
            wks.update_values('A1', [headers])
            next_row = 2
        else:
            # Use append method instead of calculating row numbers
            next_row = None  # We'll use append method
        
        # Prepare new row data with proper formatting
        new_row = [
            str(payment_data.get('tx_ref', '')),
            str(payment_data.get('user_id', '')),
            str(payment_data.get('course_id', '')),
            str(payment_data.get('price', '')),
            payment_data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            str(payment_data.get('payment_method', 'Unknown'))
        ]
        
        print(f"🔍 Debug - Adding row data: {new_row}")
        
        # Use append method which is more reliable
        try:
            wks.append_table(new_row)
            print(f"✅ Payment added to Google Sheets: {payment_data.get('tx_ref', 'Unknown')}")
            return True
        except Exception as append_error:
            print(f"❌ Append method failed: {append_error}")
            # Fallback: try to add to specific row if we calculated one
            if next_row:
                try:
                    wks.update_values(f'A{next_row}', [new_row])
                    print(f"✅ Payment added using fallback method: {payment_data.get('tx_ref', 'Unknown')}")
                    return True
                except Exception as fallback_error:
                    print(f"❌ Fallback method also failed: {fallback_error}")
                    return False
            else:
                return False
        
    except Exception as e:
        print(f"❌ Error adding payment to Google Sheets: {e}")
        return False

def sync_all_payments_to_sheets():
    """
    Sync all payments from database to Google Sheets (useful for initial setup)
    """
    try:
        if not os.path.exists(DB_PATH):
            print(f"Database file not found: {DB_PATH}")
            return False
        
        wks = get_google_sheets_connection()
        if not wks:
            return False
        
        # Get all payments from database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT tx_ref, user_id, course_id, price FROM payments ORDER BY rowid")
        payments = cursor.fetchall()
        conn.close()
        
        if not payments:
            print("No payments found in database")
            return True
        
        # Prepare data for Google Sheets
        headers = ['tx_ref', 'user_id', 'course_id', 'price', 'timestamp', 'payment_method']
        data = [headers]
        
        for payment in payments:
            row = list(payment) + [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Unknown']
            data.append(row)
        
        # Clear sheet and upload all data
        wks.clear()
        wks.update_values('A1', data)
        print(f"✅ Synced {len(payments)} payments to Google Sheets")
        return True
        
    except Exception as e:
        print(f"❌ Error syncing payments to Google Sheets: {e}")
        return False

def get_payment_count():
    """Get total number of payments in the database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM payments")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        print(f"Error getting payment count: {e}")
        return 0

def test_google_sheets_connection():
    """Test function to debug Google Sheets connection and data writing"""
    print("🧪 Testing Google Sheets connection and data writing...")
    
    # Test 1: Check connection
    print("\n1. Testing connection...")
    wks = get_google_sheets_connection()
    if wks:
        print("✅ Connection successful")
    else:
        print("❌ Connection failed")
        return False
    
    # Test 2: Check current sheet data
    print("\n2. Checking current sheet data...")
    try:
        current_data = wks.get_all_values()
        print(f"📊 Current rows in sheet: {len(current_data)}")
        if current_data:
            print(f"📋 Headers: {current_data[0]}")
            if len(current_data) > 1:
                print(f"📋 Last row: {current_data[-1]}")
    except Exception as e:
        print(f"❌ Error reading sheet data: {e}")
    
    # Test 3: Add test payment
    print("\n3. Adding test payment...")
    sample_payment = {
        'tx_ref': f'TEST_{datetime.now().strftime("%H%M%S")}',
        'user_id': 99999,
        'course_id': 99,
        'price': 999.99,
        'payment_method': 'Test'
    }
    
    result = add_payment_to_sheets(sample_payment)
    print(f"📝 Test result: {result}")
    
    # Test 4: Verify data was added
    print("\n4. Verifying data was added...")
    try:
        updated_data = wks.get_all_values()
        print(f"📊 Updated rows in sheet: {len(updated_data)}")
        if len(updated_data) > len(current_data):
            print("✅ New row was added!")
            print(f"📋 New last row: {updated_data[-1]}")
        else:
            print("❌ No new row was added")
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
    
    return result

# Test function
if __name__ == "__main__":
    test_google_sheets_connection()
