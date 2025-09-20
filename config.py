import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
API_TOKEN = os.getenv("API_TOKEN", "8279369881:AAHs1Wntr3BOhEfz9wvV1RLM4AJ8oYfg2OU")

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://mavgnxpzbubhckynydls.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_secret_9Q50nd-djnB6iuUmB-_ulg_67xIYnxb")

# Supabase Client Setup
from supabase import create_client, Client

if not SUPABASE_URL or not SUPABASE_KEY or SUPABASE_URL == "https://your-project-id.supabase.co" or SUPABASE_KEY == "your-supabase-api-key-here":
    raise ValueError("Please update SUPABASE_URL and SUPABASE_KEY in config.py with your actual Supabase credentials")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase_client() -> Client:
    """Get the Supabase client instance"""
    return supabase
GROUP_ID = -1002522899966  # your supergroup ID
BOT_MEDIA_THREAD_ID = 52  # replace with the actual thread ID
SUPPORT_USERNAME = "@SemayCreatives_support"
SOCIAL_LINKS = {
    "Instagram": "https://instagram.com/semaycreatives",
    "Facebook": "https://facebook.com/semaycreatives",
    "YouTube": "https://youtube.com/@semaycreatives"
}
ABOUT_TEXT = (
    "🛡️ *About Us?*\n"
    "Semay Creatives is a leading provider of creative courses in Ethiopia.\n"
    "We offer a refund policy, secure payments, and have helped hundreds of students.\n"
    "Check our social media for testimonials!"
)
HELP_TEXT = (
    "❓ *Help*\n"
    "Welcome to Semay Creatives!\n\n"
    "• Tap *Courses* to explore available courses and view your purchased ones.\n"
    "• Tap *Check Courses* to see all our current offerings with details and previews.\n"
    "• Tap *My Courses* to view courses you have purchased (coming soon).\n"
    "• Tap *Contact Support* if you need assistance or want to buy a course.\n"
    "• Tap *FAQ* for answers to common questions about payment, access, and refunds.\n"
    "• Tap *About Us* to learn more about Semay Creatives and our mission.\n"
    "• Tap *Social Media* to connect with us on Instagram, Facebook, and YouTube.\n\n"
    "If you need further help, just reach out to our support team!"
)
FAQ_TEXT = (
    "💬 *FAQ*\n"
    "• *How do I buy a course?* Contact support and follow instructions.\n"
    "• *How do I access my course?* You'll be added to a private Telegram channel.\n"
    "• *Is there a refund?* Yes, within the stated refund period.\n"
    "• *Who do I contact for help?* Use the Contact Support button."
)

# Payment Settings
PAYMENT_SETTINGS = {
    "telebirr": {
        "receiver_name": "TESFAYE MEKONEN KABE",
        "receiver_account": "2519****6789",
        "currency": "ETB"
    },
    "cbe": {
        "receiver_name": "Teyiba Seyid Ebrahim",
        "receiver_account": "1****6431",
        "currency": "ETB"
    }

}

# API Configuration
API_KEY = "Y21leHR0eG9nMDAwb25xMGtqOG9qdmhsbS0xNzU2NTMyMDYyMjUzLTBxbHNqbWwxYTBy"