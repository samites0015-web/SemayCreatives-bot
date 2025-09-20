#!/usr/bin/env python3
"""
Initialize Supabase database with required tables and demo data
Run this once to set up your Supabase database
"""

from config import get_supabase_client

def create_tables():
    """Create the required tables in Supabase"""
    print("📋 Creating database tables...")
    
    # Note: In Supabase, tables are typically created through the dashboard
    # or using SQL scripts. This is just a reference for the schema.
    
    tables_sql = """
    -- Admins table
    CREATE TABLE IF NOT EXISTS admins (
        telegram_id BIGINT PRIMARY KEY
    );

    -- Courses table
    CREATE TABLE IF NOT EXISTS courses (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        refund_days INTEGER NOT NULL,
        poster_id TEXT,
        showreel_id TEXT,
        invite_link TEXT
    );

    -- Payments table
    CREATE TABLE IF NOT EXISTS payments (
        tx_ref TEXT PRIMARY KEY,
        user_id BIGINT NOT NULL,
        course_id INTEGER NOT NULL REFERENCES courses(id),
        price DECIMAL(10,2) NOT NULL,
        purchased_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Users table for language preference
    CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT PRIMARY KEY,
        language TEXT DEFAULT 'en'
    );
    """
    
    print("✅ Table schemas ready. Please create these tables in your Supabase dashboard:")
    print(tables_sql)
    return True

def insert_demo_data():
    """Insert demo data into Supabase"""
    print("📊 Inserting demo data...")
    
    try:
        supabase = get_supabase_client()
        
        # Insert demo admin
        admin_data = {"telegram_id": 123456789}
        supabase.table('admins').insert(admin_data).execute()
        print("✅ Demo admin inserted")
        
        # Insert demo course
        course_data = {
            "id": 1,
            "name": "Video Editing",
            "price": 200.0,
            "refund_days": 2,
            "poster_id": "AgACAgQAAyEFAASWYGX-AANTaLrpQmS1frSSElYNBK8-T2_CGM4AArTRMRtFrtFRam2q7lWKGYkBAAMCAAN5AAM2BA",
            "showreel_id": "BAACAgQAAyEFAASWYGX-AANPaLrSwz4SounRBKPV7kxNu6ho-CUAAg0fAAJFrtFRYrD03GLWLXk2BA",
            "invite_link": "https://t.me/+example_invite_link"
        }
        supabase.table('courses').insert(course_data).execute()
        print("✅ Demo course inserted")
        
        # Insert demo payment
        payment_data = {
            "tx_ref": "demo_tx_001",
            "user_id": 123456789,
            "course_id": 1,
            "price": 300.0
        }
        supabase.table('payments').insert(payment_data).execute()
        print("✅ Demo payment inserted")
        
        return True
        
    except Exception as e:
        print(f"❌ Error inserting demo data: {e}")
        return False

def test_connection():
    """Test the Supabase connection"""
    print("🔌 Testing Supabase connection...")
    
    try:
        supabase = get_supabase_client()
        # Try to fetch from a table to test connection
        response = supabase.table('courses').select('count').execute()
        print("✅ Supabase connection successful!")
        return True
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        print("Please check your SUPABASE_URL and SUPABASE_KEY in your .env file")
        return False

if __name__ == "__main__":
    print("🚀 Initializing Supabase database...")
    print()
    
    # Test connection first
    if not test_connection():
        exit(1)
    
    print()
    
    # Create tables (reference only)
    create_tables()
    
    print()
    
    # Insert demo data
    if insert_demo_data():
        print()
        print("🎉 Supabase initialization completed successfully!")
        print("📊 Your bot is now ready to use Supabase as the database backend.")
    else:
        print("❌ Initialization failed. Please check your Supabase configuration.")
