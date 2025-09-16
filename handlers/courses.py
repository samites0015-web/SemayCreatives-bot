from db import get_all_courses, get_course
from keyboards.keyboards import courses_menu_markup,courses_back_markup, main_menu_markup, payment_method_markup, cancel_payment_markup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

import sqlite3

DB_PATH = "data/main.db"
PAY_PHONE = "+251924146789"
PAY_NAME = "TESFAYE MEKONEN KABE"

# Store pending course for each user
pending_course = {}

# Track users waiting for transaction ID
waiting_for_tx = set()

def register_course_handlers(bot):
    # BLOCK inline buttons if waiting for transaction id (must be first)
    @bot.callback_query_handler(func=lambda call: call.from_user.id in waiting_for_tx)
    def block_inline_buttons(call):
        bot.answer_callback_query(call.id, "Please finish your payment process or press ❌ Cancel Payment to cancel.")

    @bot.message_handler(func=lambda m: m.from_user.id in waiting_for_tx and m.text != "❌ Cancel Payment")
    def block_other_requests(message):
        bot.send_message(
            message.chat.id,
            "Please finish your payment process or press ❌ Cancel Payment to cancel."
        )
        # Re-register the transaction handler so the user stays in the payment flow
        bot.register_next_step_handler(message, process_transaction_id)

    @bot.message_handler(func=lambda m: m.text and m.text.strip() == "📚 Check Courses")
    def show_courses(message):
        if message.chat.type != "private":
            return
        chat_id = message.chat.id
        courses = get_all_courses()
        for course_id, course in courses.items():
            caption = (
                f"🎓 *{course['name']}*\n"
                f"💰 *Price:* {course['price']} birr\n"
                f"⏳ *Refund:* {course['refund_days']} days\n"
                f"🔗 *Access:* Private Telegram Channel"
            )
            details_markup = InlineKeyboardMarkup()
            details_markup.add(
                InlineKeyboardButton("ℹ️ Show More Details", callback_data=f"details_{course_id}")
            )
            details_markup.add(
                InlineKeyboardButton("🛒 Buy Now!", callback_data=f"buy_{course_id}")
            )
            try:
                bot.send_photo(chat_id, course.get("poster_id", ""), caption=caption, parse_mode="Markdown", reply_markup=details_markup)
            except Exception as e:
                bot.send_message(chat_id, f"Poster not available. Error: {e}")
        bot.send_message(
            message.chat.id,
            "✨ All courses listed above.",
            reply_markup=courses_back_markup()
        )

    @bot.message_handler(func=lambda m: m.text and m.text.strip() == "🗂️ My Courses")
    def my_courses(message):
        if message.chat.type != "private":
            return
        chat_id = message.chat.id
        user_id = message.from_user.id
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT course_id FROM payments WHERE user_id=?", (user_id,))
        course_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        if not course_ids:
            bot.send_message(
                chat_id,
                "🗂️ You have not purchased any courses yet.\nBrowse available courses with \n*📚 Check Courses.*",
                reply_markup=courses_back_markup(),
                parse_mode="Markdown"
            )
        else:
            for cid in course_ids:
                course = get_course(cid)
                if not course:
                    continue
                caption = (
                    f"🎓 *{course['name']}*\n"
                    f"💰 *Price:* {course['price']} birr\n"
                    f"🔗 *Access:* Private Telegram Channel"
                )
                markup = InlineKeyboardMarkup()
                if course.get("invite_link"):
                    markup.add(
                        InlineKeyboardButton("🔗 Join Channel", url=course["invite_link"])
                    )
                markup.add(
                    InlineKeyboardButton("💸 Refund", callback_data=f"refund_{cid}")
                )
                try:
                    bot.send_photo(chat_id, course.get("poster_id", ""), caption=caption, parse_mode="Markdown", reply_markup=markup)
                except Exception:
                    bot.send_message(chat_id, caption, parse_mode="Markdown", reply_markup=markup)
            bot.send_message(
                chat_id,
                "🗂️ All your purchased courses are listed above.",
                reply_markup=courses_back_markup()
            )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("details_"))
    def show_details(call):
        if call.message.chat.type != "private":
            return
        course_id = call.data.split("_", 1)[1]
        course = get_course(course_id)
        if not course:
            bot.answer_callback_query(call.id, "Course not found.")
            return
        caption = (
            f"🎬 *See what you'll learn in this course!*"
        )
        buy_markup = InlineKeyboardMarkup()
        buy_markup.add(
            InlineKeyboardButton("🛒 Buy Course", callback_data=f"buy_{course_id}")
        )
        try:
            bot.send_video(call.message.chat.id, course.get("showreel_id", ""), caption=caption, parse_mode="Markdown", reply_markup=buy_markup)
        except Exception as e:
            bot.send_message(call.message.chat.id, "Showreel not available.")
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("buy_") or call.data.startswith("buynow_"))
    def buy_course(call):
        if call.message.chat.type != "private":
            return
        if call.data.startswith("buy_"):
            course_id = int(call.data.split("_", 1)[1])
        elif call.data.startswith("buynow_"):
            course_id = int(call.data.split("_", 1)[1])
        else:
            bot.answer_callback_query(call.id, "Invalid action.")
            return
        course = get_course(course_id)
        if not course:
            bot.answer_callback_query(call.id, "Course not found.")
            return

        pending_course[call.from_user.id] = course_id
        bot.send_message(
            call.message.chat.id,
            "Choose payment method:",
            reply_markup=payment_method_markup()
        )

    @bot.message_handler(func=lambda m: m.text == "💸 Telebirr")
    def telebirr_selected(message):
        user_id = message.from_user.id
        if user_id not in pending_course:
            bot.send_message(message.chat.id, "No course selected. Please choose a course first.")
            return
        waiting_for_tx.add(user_id)
        bot.send_message(
            message.chat.id,
            "Please enter your transaction ID:",
            reply_markup=cancel_payment_markup()
        )
        bot.register_next_step_handler(message, process_transaction_id)

    def process_transaction_id(message):
        user_id = message.from_user.id
        if message.text == "❌ Cancel Payment":
            pending_course.pop(user_id, None)
            waiting_for_tx.discard(user_id)
            bot.send_message(
                message.chat.id,
                "Payment cancelled. You can start again.",
                reply_markup=courses_menu_markup()
            )
            return
        course_id = pending_course.pop(user_id, None)
        waiting_for_tx.discard(user_id)
        if not course_id:
            bot.send_message(message.chat.id, "No course selected. Please choose a course first.")
            return
        course = get_course(course_id)
        if not course:
            bot.send_message(message.chat.id, "Course not found.")
            return
        # Store payment in DB (no verification)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO payments (tx_ref, user_id, course_id, price) VALUES (?, ?, ?, ?)",
            (message.text.strip(), user_id, course_id, float(course['price']))
        )
        conn.commit()
        conn.close()
        bot.send_message(
            message.chat.id,
            "✅ Payment approved! The course has been added to your account. Access it from *My Courses*.",
            parse_mode="Markdown",
            reply_markup=courses_menu_markup()
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("refund_"))
    def refund_course(call):
        bot.answer_callback_query(call.id, "Refund feature coming soon!")
        
    @bot.message_handler(func=lambda m: m.text == "⬅️ Courses")
    def back_to_courses(message):
        bot.send_message(
            message.chat.id,
            "Returned to the courses menu.",
            reply_markup=courses_menu_markup()
        )