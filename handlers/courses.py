from supabase_db import get_all_courses, get_course, add_payment, get_user_payments, is_transaction_used
from keyboards.keyboards import courses_menu_markup,courses_back_markup, main_menu_markup, payment_method_markup, cancel_payment_markup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import PAYMENT_SETTINGS, API_KEY
from handlers.parse_receipt import verify_telebirr, verify_cbe


# Store pending course for each user
pending_course = {}

# Track users waiting for transaction ID
waiting_for_tx = set()

# Track payment method for each user
pending_payment_method = {}


def register_course_handlers(bot):
    # BLOCK inline buttons if waiting for transaction id (must be first)
    @bot.callback_query_handler(func=lambda call: call.from_user.id in waiting_for_tx)
    def block_inline_buttons(call):
        bot.answer_callback_query(call.id, "Please finish your payment process or press ❌ Cancel Payment to cancel.")

    @bot.message_handler(func=lambda m: m.from_user.id in waiting_for_tx and m.text != "❌ Cancel Payment")
    def block_other_requests(message):
        user_id = message.from_user.id
        payment_method = pending_payment_method.get(user_id, "telebirr")
        
        bot.send_message(
            message.chat.id,
            "Please finish your payment process or press ❌ Cancel Payment to cancel."
        )
        
        # Re-register the appropriate handler based on payment method
        if payment_method == "cbe":
            bot.register_next_step_handler(message, process_cbe_transaction_id)
        else:
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
        course_ids = get_user_payments(user_id)
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
        pending_payment_method[user_id] = "telebirr"
        waiting_for_tx.add(user_id)
        bot.send_message(
            message.chat.id,
            "Please enter your Telebirr transaction ID:",
            reply_markup=cancel_payment_markup()
        )
        bot.register_next_step_handler(message, process_transaction_id)

    @bot.message_handler(func=lambda m: m.text == "🏦 CBE")
    def cbe_selected(message):
        user_id = message.from_user.id
        if user_id not in pending_course:
            bot.send_message(message.chat.id, "No course selected. Please choose a course first.")
            return
        pending_payment_method[user_id] = "cbe"
        waiting_for_tx.add(user_id)
        bot.send_message(
            message.chat.id,
            "Please enter your CBE transaction ID:",
            reply_markup=cancel_payment_markup()
        )
        bot.register_next_step_handler(message, process_cbe_transaction_id)

    def process_cbe_transaction_id(message):
        user_id = message.from_user.id
        if message.text == "❌ Cancel Payment":
            pending_course.pop(user_id, None)
            pending_payment_method.pop(user_id, None)
            waiting_for_tx.discard(user_id)
            bot.send_message(
                message.chat.id,
                "Payment cancelled. You can start again.",
                reply_markup=courses_menu_markup()
            )
            return
        
        # Store transaction ID and ask for account number
        pending_course[user_id] = {
            'course_id': pending_course[user_id],
            'txn_id': message.text.strip()
        }
        bot.send_message(
            message.chat.id,
            "Please enter the last 8 digits of your CBE account number:",
            reply_markup=cancel_payment_markup()
        )
        bot.register_next_step_handler(message, process_cbe_account_number)

    def process_cbe_account_number(message):
        user_id = message.from_user.id
        if message.text == "❌ Cancel Payment":
            pending_course.pop(user_id, None)
            pending_payment_method.pop(user_id, None)
            waiting_for_tx.discard(user_id)
            bot.send_message(
                message.chat.id,
                "Payment cancelled. You can start again.",
                reply_markup=courses_menu_markup()
            )
            return
        
        # Get the stored transaction ID and course info
        course_data = pending_course[user_id]
        course_id = course_data['course_id']
        txn_id = course_data['txn_id']
        account_last_8 = message.text.strip()
        
        # Verify CBE payment
        verification_result = verify_cbe_payment(txn_id, account_last_8, course_id)
        
        if verification_result == "DUPLICATE":
            bot.send_message(
                message.chat.id,
                "❌ This transaction ID has already been used. Each transaction can only be used once for course purchases.",
                reply_markup=courses_menu_markup()
            )
            # Clean up
            pending_course.pop(user_id, None)
            pending_payment_method.pop(user_id, None)
            waiting_for_tx.discard(user_id)
        elif verification_result:
            # Store payment in Supabase
            add_payment(txn_id, user_id, course_id, float(get_course(course_id)['price']))
            
            
            # Clean up
            pending_course.pop(user_id, None)
            pending_payment_method.pop(user_id, None)
            waiting_for_tx.discard(user_id)
            
            bot.send_message(
                message.chat.id,
                "✅ Payment approved! The course has been added to your account. Access it from *My Courses*.",
                parse_mode="Markdown",
                reply_markup=courses_menu_markup()
            )
        else:
            bot.send_message(
                message.chat.id,
                "❌ Payment verification failed. Please check your transaction details and try again.",
                reply_markup=courses_menu_markup()
            )
            # Clean up
            pending_course.pop(user_id, None)
            pending_payment_method.pop(user_id, None)
            waiting_for_tx.discard(user_id)

    def process_transaction_id(message):
        user_id = message.from_user.id
        if message.text == "❌ Cancel Payment":
            pending_course.pop(user_id, None)
            pending_payment_method.pop(user_id, None)
            waiting_for_tx.discard(user_id)
            bot.send_message(
                message.chat.id,
                "Payment cancelled. You can start again.",
                reply_markup=courses_menu_markup()
            )
            return
        
        course_id = pending_course.pop(user_id, None)
        payment_method = pending_payment_method.pop(user_id, None)
        waiting_for_tx.discard(user_id)
        
        if not course_id:
            bot.send_message(message.chat.id, "No course selected. Please choose a course first.")
            return
        
        course = get_course(course_id)
        if not course:
            bot.send_message(message.chat.id, "Course not found.")
            return
        
        # Verify Telebirr payment
        verification_result = verify_telebirr_payment(message.text.strip(), course_id)
        
        if verification_result == "DUPLICATE":
            bot.send_message(
                message.chat.id,
                "❌ This transaction ID has already been used. Each transaction can only be used once for course purchases.",
                reply_markup=courses_menu_markup()
            )
        elif verification_result:
            # Store payment in Supabase
            add_payment(message.text.strip(), user_id, course_id, float(course['price']))
            
            
            bot.send_message(
                message.chat.id,
                "✅ Payment approved! The course has been added to your account. Access it from *My Courses*.",
                parse_mode="Markdown",
                reply_markup=courses_menu_markup()
            )
        else:
            bot.send_message(
                message.chat.id,
                "❌ Payment verification failed. Please check your transaction details and try again.",
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

def verify_telebirr_payment(transaction_id, course_id):
    """
    Verify Telebirr payment using the new API service
    """
    try:
        # First check if transaction ID has already been used
        if is_transaction_used(transaction_id):
            return "DUPLICATE"
        
        course = get_course(course_id)
        if not course:
            return False
        
        # Verify payment using the new API
        api_response = verify_telebirr(transaction_id, API_KEY)
        
        # Check if API call was successful
        if not api_response.get("success", False):
            return False
        
        receipt_data = api_response.get("data", {})
        
        # Verify payment details
        settings = PAYMENT_SETTINGS["telebirr"]
        required_amount = float(course['price'])
        
        # Extract amount from totalPaidAmount string (e.g., "1616.00 Birr" -> 1616.00)
        total_paid_str = receipt_data.get('totalPaidAmount', '0 Birr')
        try:
            actual_amount = float(total_paid_str.split()[0])
        except (ValueError, IndexError):
            actual_amount = 0
        
        # Check if payment is valid
        name_match = receipt_data.get("creditedPartyName") == settings["receiver_name"]
        account_match = receipt_data.get("creditedPartyAccountNo") == settings["receiver_account"]
        amount_match = actual_amount >= required_amount
        status_match = receipt_data.get("transactionStatus") == "Completed"
        
        return name_match and account_match and amount_match and status_match
        
    except Exception as e:
        print(f"Error verifying Telebirr payment: {e}")
        return False

def verify_cbe_payment(transaction_id, account_last_8, course_id):
    """
    Verify CBE payment using the new API service
    """
    try:
        # First check if transaction ID has already been used
        if is_transaction_used(transaction_id):
            return "DUPLICATE"
        
        course = get_course(course_id)
        if not course:
            return False
        
        # Verify payment using the new API
        api_response = verify_cbe(transaction_id, account_last_8, API_KEY)
        
        # Check if API call was successful
        if not api_response.get("success", False):
            return False
        
        # CBE API returns data directly, not nested under 'data' key
        receipt_data = api_response
        
        # Verify payment details
        settings = PAYMENT_SETTINGS["cbe"]
        required_amount = float(course['price'])
        
        # CBE API returns amount as integer, not string
        actual_amount = receipt_data.get("amount", 0)
        
        # Check if payment is valid
        name_match = receipt_data.get("receiver") == settings["receiver_name"]
        account_match = receipt_data.get("receiverAccount") == settings["receiver_account"]
        amount_match = actual_amount >= required_amount
        # CBE API doesn't have a status field, but if we get data, it's successful
        
        return name_match and account_match and amount_match
        
    except Exception as e:
        print(f"Error verifying CBE payment: {e}")
        return False