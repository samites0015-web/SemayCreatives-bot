# Updated bot without language selection (can be added later)
# Requires: pip install pyTelegramBotAPI, requests
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import json
import config

bot = telebot.TeleBot(config.API_TOKEN)

# Load courses from JSON
with open("data/courses.json", "r", encoding="utf-8") as f:
    courses = json.load(f)

STATE_START = "START"
STATE_VIEWING_COURSE = "VIEWING_COURSE"

user_state = {}

def set_state(chat_id, state):
    user_state[chat_id] = state

def get_state(chat_id):
    return user_state.get(chat_id, STATE_START)

def send_video_if_exists(chat_id, file_id, caption=""):
    if not file_id:
        return
    try:
        bot.send_video(chat_id, file_id, caption=caption, parse_mode="Markdown")
    except:
        pass

def main_menu_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("🎓 Courses"))
    markup.row(
        KeyboardButton("❓ Help"),
        KeyboardButton("🛡️ About Us")
    )
    markup.row(
        KeyboardButton("💬 FAQ"),
        KeyboardButton("📞 Contact Support"),
        KeyboardButton("🌐 Social Media")
    )
    return markup

def courses_menu_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("📚 Check Courses"), KeyboardButton("🗂️ My Courses"))
    markup.row(KeyboardButton("⬅️ Back to Main Menu"))
    return markup

@bot.message_handler(commands=['start'])
def cmd_start(message):
    chat_id = message.chat.id
    set_state(chat_id, STATE_START)
    bot.send_message(
        chat_id,
        "👋 Welcome to Semay Creatives!\nChoose an option below:",
        reply_markup=main_menu_markup()
    )

@bot.message_handler(func=lambda m: m.text and m.text.strip() == "🎓 Courses")
def courses_menu(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "🎓 Courses Menu:\nChoose an option below.",
        reply_markup=courses_menu_markup()
    )

@bot.message_handler(func=lambda m: m.text and m.text.strip() == "⬅️ Back to Main Menu")
def back_to_main_menu(message):
    cmd_start(message)

@bot.message_handler(func=lambda m: m.text and m.text.strip() == "📚 Check Courses")
def show_courses(message):
    chat_id = message.chat.id
    set_state(chat_id, STATE_VIEWING_COURSE)
    for course_id, course in courses.items():
        caption = (
            f"🎓 *{course['name']}*\n"
            f"💰 *Price:* {course['price']} birr\n"
            f"⏳ *Refund:* {course['refund_days']} days\n"
            f"🔗 *Access:* Private Telegram Channel"
        )
        details_markup = InlineKeyboardMarkup()
        details_markup.add(InlineKeyboardButton("Show More Details", callback_data=f"details_{course_id}"))
        try:
            bot.send_photo(chat_id, course.get("poster_id", ""), caption=caption, parse_mode="Markdown", reply_markup=details_markup)
        except Exception as e:
            bot.send_message(chat_id, f"Poster not available. Error: {e}")
    bot.send_message(chat_id, "✨ All courses listed above.", parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text and m.text.strip() == "🗂️ My Courses")
def my_courses(message):
    chat_id = message.chat.id
    # Placeholder: Replace with actual purchased courses logic
    bot.send_message(
        chat_id,
        "🗂️ You have not purchased any courses yet.\nBrowse available courses with \n*📚 Check Courses.*",
        reply_markup=courses_menu_markup(),
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda m: m.text and m.text.strip() == "❓ Help")
def help_handler(message):
    bot.send_message(message.chat.id, config.HELP_TEXT, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text and m.text.strip() == "🛡️ About Us")
def about_handler(message):
    bot.send_message(message.chat.id, config.ABOUT_TEXT, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text and m.text.strip() == "💬 FAQ")
def faq_handler(message):
    bot.send_message(message.chat.id, config.FAQ_TEXT, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text and m.text.strip() == "📞 Contact Support")
def contact_handler(message):
    bot.send_message(
        message.chat.id,
        f"📞 Contact Support\nReach us at {config.SUPPORT_USERNAME}",
        parse_mode=None
    )

@bot.message_handler(func=lambda m: m.text and m.text.strip() == "🌐 Social Media")
def social_handler(message):
    links = "\n".join([f"• [{name}]({url})" for name, url in config.SOCIAL_LINKS.items()])
    bot.send_message(
        message.chat.id,
        f"🌐 *Social Media*\n{links}",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

@bot.message_handler(func=lambda m: True)
def handle_all_text(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "I didn't understand that. Use the menu buttons. Try /start to go back to the main menu.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("details_"))
def show_details(call):
    course_id = call.data.split("_", 1)[1]
    course = courses.get(course_id)
    if not course:
        bot.answer_callback_query(call.id, "Course not found.")
        return
    caption = (
        f"🎬 *See what you'll learn in this course!*"
    )
    buy_markup = InlineKeyboardMarkup()
    buy_markup.add(InlineKeyboardButton("Buy Course", callback_data=f"buy_{course_id}"))
    # Try to send the showreel video if available
    try:
        bot.send_video(call.message.chat.id, course.get("showreel_id", ""), caption=caption, parse_mode="Markdown", reply_markup=buy_markup)
    except Exception as e:
        bot.send_message(call.message.chat.id, "Showreel not available.")
    bot.answer_callback_query(call.id)

if __name__ == "__main__":
    print("🤖 Bot running...")
    bot.infinity_polling()
