# Supabase Setup Guide

This guide will help you migrate your Telegram bot from SQLite to Supabase.

## Prerequisites

1. A Supabase account (sign up at https://supabase.com)
2. Python 3.7 or higher

## Step 1: Create Supabase Project

1. Go to https://supabase.com and sign in
2. Click "New Project"
3. Choose your organization
4. Enter project details:
   - Name: `semaycreatives-bot`
   - Database Password: (choose a strong password)
   - Region: (choose closest to your users)
5. Click "Create new project"
6. Wait for the project to be created (2-3 minutes)

## Step 2: Get Supabase Credentials

1. In your Supabase dashboard, go to **Settings** → **API**
2. Copy the following values:
   - **Project URL** (looks like: `https://your-project-id.supabase.co`)
   - **API Key** (anon/public key, looks like: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`)

## Step 3: Create Database Tables

1. In your Supabase dashboard, go to **SQL Editor**
2. Click "New Query"
3. Copy and paste this SQL script:

```sql
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
```

4. Click "Run" to execute the script

## Step 4: Configure Supabase Credentials

1. Open `config.py` in your project
2. Update the Supabase configuration with your actual credentials:

```python
# Supabase Configuration
SUPABASE_URL = "https://your-actual-project-id.supabase.co"
SUPABASE_KEY = "your-actual-supabase-api-key-here"
```

3. (Optional) You can also create a `.env` file to override these values:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-api-key-here
API_TOKEN=your-telegram-bot-token-here
```

## Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 6: Initialize Database

```bash
python init_supabase.py
```

This will:
- Test your Supabase connection
- Insert demo data (admin, course, payment)

## Step 7: Test Your Bot

```bash
python main.py
```

## Troubleshooting

### Connection Issues
- Verify your SUPABASE_URL and SUPABASE_KEY are correct
- Check that your Supabase project is active
- Ensure your IP is not blocked (if using IP restrictions)

### Database Errors
- Make sure all tables were created successfully
- Check the Supabase logs in the dashboard
- Verify your API key has the correct permissions

### Bot Issues
- Check that your API_TOKEN is valid
- Test with a simple message to your bot
- Check the bot logs for any error messages

## Migration from SQLite

If you have existing data in SQLite:

1. Export your data from the old database
2. Use the Supabase dashboard to import the data
3. Or create a migration script to transfer data programmatically

## Security Notes

- Never commit your `.env` file to version control
- Use environment variables in production
- Consider using Supabase Row Level Security (RLS) for additional security
- Regularly rotate your API keys

## Support

If you encounter issues:
1. Check the Supabase documentation
2. Review the bot logs
3. Test individual components (connection, database operations)
4. Contact support if needed
