import config

def register_support_handlers(bot):
    @bot.message_handler(func=lambda m: m.text and m.text.strip() == "❓ Help")
    def help_handler(message):
        if message.chat.type != "private":
            return
        bot.send_message(message.chat.id, config.HELP_TEXT, parse_mode="Markdown")

    @bot.message_handler(func=lambda m: m.text and m.text.strip() == "🛡️ About Us")
    def about_handler(message):
        if message.chat.type != "private":
            return
        bot.send_message(message.chat.id, config.ABOUT_TEXT, parse_mode="Markdown")

    @bot.message_handler(func=lambda m: m.text and m.text.strip() == "💬 FAQ")
    def faq_handler(message):
        if message.chat.type != "private":
            return
        bot.send_message(message.chat.id, config.FAQ_TEXT, parse_mode="Markdown")

    @bot.message_handler(func=lambda m: m.text and m.text.strip() == "📞 Contact Support")
    def contact_handler(message):
        if message.chat.type != "private":
            return
        bot.send_message(
            message.chat.id,
            f"📞 Contact Support\nReach us at {config.SUPPORT_USERNAME}",
            parse_mode=None
        )

    @bot.message_handler(func=lambda m: m.text and m.text.strip() == "🌐 Social Media")
    def social_handler(message):
        if message.chat.type != "private":
            return
        links = "\n".join([f"• [{name}]({url})" for name, url in config.SOCIAL_LINKS.items()])
        bot.send_message(
            message.chat.id,
            f"🌐 *Social Media*\n{links}",
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

    @bot.message_handler(func=lambda m: True)
    def handle_all_text(message):
        if message.chat.type != "private":
            return
        chat_id = message.chat.id
        bot.send_message(chat_id, "I didn't understand that. Use the menu buttons. Try /start to go back to the main menu.")