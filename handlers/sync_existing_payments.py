#!/usr/bin/env python3
"""
One-time script to sync all existing payments to Google Sheets
Run this once to migrate from the old timer-based system to real-time updates
"""

from handlers.google_sheets_realtime import sync_all_payments_to_sheets

if __name__ == "__main__":
    print("🔄 Syncing all existing payments to Google Sheets...")
    print("This is a one-time migration from timer-based to real-time updates.")
    print()
    
    success = sync_all_payments_to_sheets()
    
    if success:
        print("✅ Migration completed successfully!")
        print("🎉 Your bot now uses real-time Google Sheets updates!")
        print("📊 New payments will appear in Google Sheets immediately.")
        print()
        print("⚠️  You can now stop running the old googlesheets.py timer script.")
    else:
        print("❌ Migration failed. Please check your Google Sheets configuration.")
