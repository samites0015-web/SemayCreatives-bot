from keyboards.keyboards import main_menu_markup, courses_menu_markup

def register_menu_handlers(bot):
    @bot.message_handler(commands=['start'])
    def cmd_start(message):
        if message.chat.type != "private":
            return
        bot.send_message(
            message.chat.id,
            "👋 Welcome to Semay Creaives!\nChoose an option below:",
            reply_markup=main_menu_markup()
        )

    @bot.message_handler(func=lambda m: m.text and m.text.strip() == "🎓 Courses")
    def courses_menu(message):
        if message.chat.type != "private":
            return
        bot.send_message(
            message.chat.id,
            "🎓 Courses Menu:\nChoose an option below.",
            reply_markup=courses_menu_markup()
        )

    @bot.message_handler(func=lambda m: m.text and m.text.strip() == "⬅️ Main Menu")
    def back_to_main_menu(message):
        if message.chat.type != "private":
            return
        cmd_start(message)