import config

def register_fileid_handler(bot):
    @bot.message_handler(content_types=['photo', 'video'])
    def handle_media(message):
        if (
            message.chat.id == config.GROUP_ID and
            getattr(message, "message_thread_id", None) == config.BOT_MEDIA_THREAD_ID
        ):
            if message.content_type == 'photo':
                file_id = message.photo[-1].file_id
                print(f"Photo file_id: {file_id}")
                bot.reply_to(message, f"{file_id}")
            elif message.content_type == 'video':
                file_id = message.video.file_id
                print(f"Video file_id: {file_id}")
                bot.reply_to(message, f"{file_id}")
        else:
            print(f"Ignored media from chat id: {message.chat.id}, thread id: {getattr(message, 'message_thread_id', None)}")