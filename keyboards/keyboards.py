from telebot.types import ReplyKeyboardMarkup, KeyboardButton

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
    markup.row(KeyboardButton("⬅️ Main Menu"))
    return markup

def courses_back_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("⬅️ Courses"))
    return markup

def payment_method_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("💸 Telebirr"))
    markup.add(KeyboardButton("⬅️ Courses"))
    return markup

def cancel_payment_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("❌ Cancel Payment"))
    return markup