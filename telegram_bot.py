from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, CallbackQueryHandler, InlineQueryHandler
from datetime import datetime, timedelta
from api import HiddifyApi
import logging

# Conversation states
SHOW_USER, ADD_USER = range(2)

logging.basicConfig(format='%(name)s - %(message)s', level=logging.DEBUG)

# Create a HiddifyApi instance
hiddify_api = HiddifyApi()

def start(update: Update, context: CallbackContext) -> None:
    if check_authorization(update):
        keyboard = [
            ["Add User🍀", "Show User"],
            ["Server Info🌐", "Backup File📥"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text('🧿Welcome to your Hiddify Bot 🤖!\nUse the buttons below to navigate:', reply_markup=reply_markup)

def add_user(update: Update, context: CallbackContext) -> None:
    if check_authorization(update):
        update.message.reply_text('Please provide the following information to add a new user:\n'
                                  '1. User Name\n'
                                  '2. Number of Days\n'
                                  '3. Traffic Limit (GB)\n\n'
                                  'Type each value on a new line.')

        context.user_data['state'] = ADD_USER

def process_user_info(update: Update, context: CallbackContext) -> None:
    if check_authorization(update):
        if 'state' in context.user_data:
            if context.user_data['state'] == ADD_USER:
                user_info = update.message.text.split('\n')

                if len(user_info) == 3:
                    user_name, user_days, user_traffic = user_info
                    uuid = hiddify_api.generate_uuid()
                    context.user_data['uuid'] = uuid
                    context.user_data['telegram_id'] = update.message.from_user.id
                    context.user_data['comment'] = "🤖Telegram🤖"  # You can customize this if needed

                    result = hiddify_api.add_service(
                        uuid,
                        context.user_data['comment'],
                        user_name,
                        int(user_days),
                        int(user_traffic),
                        context.user_data['telegram_id']
                    )

                    if result:
                        subscription_link = f"{hiddify_api.sublinkurl}/{uuid}/sub/"
                        qr_byte_io = hiddify_api.generate_qr_code(subscription_link)
                        
                        message = (
                            f'User added successfully\n'
                            f'User UUID: `{uuid}`\n'
                            f'Name: {user_name}\n'
                            f'Usage Limit: {user_traffic} GB\n'
                            f'Package Days: {user_days} Days\n'
                            f'SubLink : `{subscription_link}`'
                        )
                        
                        update.message.reply_photo(photo=qr_byte_io, caption=message, parse_mode='MarkdownV2')
                    else:
                        update.message.reply_text('Failed to add user. Please try again.')
                else:
                    update.message.reply_text('Invalid input. Please provide all three pieces of information.')

                del context.user_data['state']
            elif context.user_data['state'] == SHOW_USER:
                user_uuid = update.message.text
                user_info = hiddify_api.find_service(user_uuid)
                if user_info:
                    display_user_info(update, user_info)
                else:
                    update.message.reply_text('User not found.☹️')
                del context.user_data['state']
        #else:
            #update.message.reply_text('Invalid command. Please use the buttons below.')

def display_user_info(update: Update, user_info: dict) -> None:
    last_online_str = user_info.get('last_online')
    package_days = user_info.get('package_days')
    usage_limit_gb = user_info.get('usage_limit_GB')
    current_usage_gb = user_info.get('current_usage_GB')

    if last_online_str:
        try:
            last_online = datetime.fromisoformat(last_online_str)
        except ValueError:
            status_emoji = "\U00002b55"
            last_online_formatted = "Not Active"
        else:
            time_difference = datetime.now() - last_online
            if time_difference <= timedelta(minutes=2):
                status_emoji = "\U0001F7E2"
            else:
                status_emoji = "\U0001F534"
            last_online_formatted = last_online.strftime('%Y-%m-%d %H:%M:%S')
    else:
        status_emoji = "\U00002b55"
        last_online_formatted = "Not Active"

    start_date_str = user_info.get('start_date')
    if start_date_str is not None:
        start_date = datetime.fromisoformat(start_date_str)
    else:
        start_date = None

    if start_date:
        days_left = (start_date + timedelta(days=package_days)) - datetime.now()

        if days_left.days < 0:
            status_emoji = "\U0000274C"  # Red X emoji
            days_left_text = "Ended"
        else:
            days_left_text = f"{days_left.days + 1} Days Left"
    else:
        days_left_text = "User Not Active"

    subscription_link = f"{hiddify_api.sublinkurl}/{user_info['uuid']}/sub/"
    qr_byte_io = hiddify_api.generate_qr_code(subscription_link)

    response_text = (
        f"Name: {user_info['name']}\n"
        f"Package Days: {package_days}\n"
        f"Start Date: {start_date.strftime('%Y-%m-%d') if start_date else '❌'}\n"
        f"Traffic: {current_usage_gb:.2f} / {usage_limit_gb} GB\n"
        f"Status: {status_emoji}\n"
        f"Last Online: {last_online_formatted}\n"
        f"Days Left: {days_left_text}\n"
    )
    #update.message.reply_text(response_text)
    keyboard = [[InlineKeyboardButton("Reset user", callback_data=f"reset_{user_info['uuid']}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_photo(photo=qr_byte_io, caption=response_text, reply_markup=reply_markup)


def reset_user(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    uuid = query.data.split("_")[1]
    if hiddify_api.reset_user_last_reset_time(uuid):
        query.answer("User reset successfully.")
    else:
        query.answer("Failed to reset user.")


def show_user(update: Update, context: CallbackContext) -> None:
    if check_authorization(update):
        update.message.reply_text('Please enter the UUID of the user you want to show:')
        context.user_data['state'] = SHOW_USER

def server_info(update: Update, context: CallbackContext) -> None:
    if check_authorization(update):
        system_status = hiddify_api.get_system_status()

        if system_status:
            system_info = system_status.get('system', {})
            usage_history = system_status.get('usage_history', {})
            m5_online = usage_history.get('m5', {}).get('online', 'N/A')
            yesterday_online = usage_history.get('yesterday', {}).get('online', 'N/A')
            usage_today = usage_history.get('today', {}).get('usage', 0) / (1024 ** 3)
            usage_yesterday = usage_history.get('yesterday', {}).get('usage', 0) / (1024 ** 3)
            total_usage_bytes = usage_history.get('total', {}).get('usage', 0) / (1024 ** 3)
            formatted_info = (
                f"CPU Percent: {system_info.get('cpu_percent', 'N/A')}% ⚠️\n"
                f"RAM Usage: {system_info.get('ram_used', 'N/A'):.2f}GB / {system_info.get('ram_total', 'N/A'):.2f}GB 〽️\n"
                f"Disk Usage: {system_info.get('disk_used', 'N/A'):.2f}GB / {system_info.get('disk_total', 'N/A'):.2f}GB 〽️\n"
                f"Total Usage: {total_usage_bytes:.2f} GB 🛜\n"
                f"----------------------------------------\n"
                f"Yesterday Usage: {usage_yesterday:.2f} GB\n"
                f"Yesterday Online: {yesterday_online}\n"
                f"----------------------------------------\n"
                f"Today Usage: {usage_today:.2f} GB\n"
                f"Users Online: {m5_online} 🟢"
            )
            update.message.reply_text(f'Server Info (Live):\n{formatted_info}')
        else:
            update.message.reply_text('Failed to retrieve server info. Please try again.')

def backup_file(update: Update, context: CallbackContext) -> None:
    if check_authorization(update):
        backup_data = hiddify_api.backup_file()
        if backup_data:
            context.bot.send_document(update.message.chat_id, document=backup_data, filename='backup.json')
        else:
            update.message.reply_text('Failed to retrieve backup file.')

def help_command(update: Update, context: CallbackContext) -> None:
    if check_authorization(update):
        update.message.reply_text('To show a specific user, use the following command:\n'
                                  '`/show_user <UUID>`\n\n'
                                  'For example:\n'
                                  '`/show_user 12345678-1234-1234-1234-1234567890ab`\n\n'
                                  'Replace `<UUID>` with the actual UUID of the user you want to show',
                                  parse_mode='MarkdownV2')

def inline_query(update, context):
    if check_authorization(update):
        query = update.inline_query.query.strip().lower()
        if query.startswith("list"):
            query_name = query[5:].strip()
            user_list = hiddify_api.get_user_list_name(query_name)

            results = []

            if user_list:
                for user in user_list[:50]:
                    user_uuid = user['uuid']
                    user_name = user['name']
                    package_days = user['package_days']
                    usage_limit_gb = user['usage_limit_GB']
                    current_usage_gb = user['current_usage_GB']
                    last_online_str = user['last_online']

                    if last_online_str:
                        try:
                            last_online = datetime.fromisoformat(last_online_str)
                        except ValueError:
                            last_online_formatted = "Not Active"
                        else:
                            last_online_formatted = last_online.strftime('%Y/%m/%d %H:%M:%S')
                    else:
                        last_online_formatted = "Not Active"

                    title = f"{user_name}"
                    discrip = f"Traffic Limit: {usage_limit_gb:.2f} GB\n Package Days: {package_days}"
                    subscription_link = f"{hiddify_api.sublinkurl}/{user_uuid}/sub/"
                    response_text = (
                        f"ID: `{user_uuid}`\n"
                        f"Name: {user_name}\n"
                        f"Package Days: {package_days}\n"
                        f"Traffic: {current_usage_gb:.2f} / {usage_limit_gb} GB\n"
                        f"Last Online: {last_online_formatted}\n"
                        f"SubLink : `{subscription_link}`"
                    )
                    response_text = response_text.replace('.', '\\.')
                    results.append(
                        InlineQueryResultArticle(
                            id=user_uuid,
                            title=title,
                            description=discrip,
                            input_message_content=InputTextMessageContent(response_text, parse_mode='MarkdownV2')
                        )
                    )

            update.inline_query.answer(results)

def handle_text_input(update: Update, context: CallbackContext) -> None:
    text = update.message.text.lower()
    if text == 'add user🍀':
        add_user(update, context)
    elif text == 'show user':
        show_user(update, context)
    elif text == 'server info🌐':
        server_info(update, context)
    elif text == 'backup file📥':
        backup_file(update, context)
    elif text == 'help':
        help_command(update, context)
    else:
        update.message.reply_text("Invalid command. Please use the buttons below.")

def check_authorization(update: Update) -> bool:
    if update.message:
        user_id = update.message.from_user.id
        is_inline_query = False
    elif update.inline_query:
        user_id = update.inline_query.from_user.id
        is_inline_query = True
    else:
        return False

    if user_id not in hiddify_api.allowed_user_ids:
        if is_inline_query:
            update.inline_query.answer([
                InlineQueryResultArticle(
                    id="unauthorized",
                    title="Unauthorized",
                    input_message_content=InputTextMessageContent("🔐Sorry, you are not authorized to use this bot.🔐")
                )
            ])
        else:
            update.message.reply_text("🔐Sorry, you are not authorized to use this bot.🔐")
        return False
    return True


# Set up the Telegram bot
def main() -> None:
    teltoken = hiddify_api.telegram_token
    updater = Updater(teltoken)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.regex('^Add User🍀$|^Show User$|^Server Info🌐$|^Backup File📥$|^Help$'), handle_text_input))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, process_user_info))
    dp.add_handler(CallbackQueryHandler(reset_user))
    dp.add_handler(InlineQueryHandler(inline_query))


    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()