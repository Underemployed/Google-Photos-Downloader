from typing import Final
import datetime
import time
import asyncio

# pip install python-telegram-bot
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from secret_token import TELEGRAM_BOT_TOKEN, CHAT_ID, BOT_USERNAME

print("Starting up bot...")
from send_photo_data import filter_photos

TOKEN: Final = TELEGRAM_BOT_TOKEN
BOT_USERNAME: Final = BOT_USERNAME
start_date = None
end_date = None


# Lets us use the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global start_date

    await update.message.reply_text(
        "Please enter the start date in the format dd-mm-yyyy"
    )
    context.user_data["awaiting_start_date"] = True


# Lets us use the /end command
async def end_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global end_date
    await update.message.reply_text(
        "Please enter the end date in the format dd-mm-yyyy"
    )
    context.user_data["awaiting_end_date"] = True


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global start_date, end_date  # Declare start_date and end_date as global

    # Get basic info of the incoming message
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Check if we are waiting for the start date
    if context.user_data.get("awaiting_start_date"):
        try:
            start_date = datetime.datetime.strptime(text, "%d-%m-%Y").date()
            context.user_data["awaiting_start_date"] = False
            await update.message.reply_text("Start date received.")
        except ValueError:
            await update.message.reply_text(
                "Incorrect date format. Please enter the start date in the format dd-mm-yyyy"
            )
            context.user_data["awaiting_start_date"] = True

        return

    # Check if we are waiting for the end date
    if context.user_data.get("awaiting_end_date"):
        try:
            end_date = datetime.datetime.strptime(text, "%d-%m-%Y").date()
            context.user_data["awaiting_end_date"] = False
            await update.message.reply_text("End date received.")
        except ValueError:
            await update.message.reply_text(
                "Incorrect date format. Please enter the end date in the format dd-mm-yyyy"
            )
            context.user_data["awaiting_end_date"] = True

        return


# /send command
async def send_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global start_date, end_date  # Declare start_date and end_date as global
    print("Sending files..." + f"\n{start_date}" + f"\n{end_date}")
    bot = context.bot
    failed_files = []
    if start_date is not None and end_date is not None:
        # Check if the chat ID of the update is the same as the target chat ID
        if update.message.from_user.username != CHAT_ID[1::]:
            print(update.message)
            print("Unauthorized chat ID. Skipping...")
            await update.message.reply_text("Who are you?")

            return

        media_items = filter_photos(start_date, end_date)
        for media_item in media_items:
            url = media_item["url"]
            file_name = media_item["filename"]
            mime_type = media_item["mimeType"]
            try:
                print(f"Sending {file_name}...", end="  ")

                await asyncio.wait_for(
                    bot.send_document(
                        chat_id=update.message.chat_id,
                        document=url,
                        filename=file_name,
                    ),
                    timeout=120,
                )
                print("Successful")
            except Exception as e:
                print("Error:", e)
        await update.message.reply_text("Done!")
    else:
        await update.message.reply_text("Please set both start and end dates.")


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


# Run the program
if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("end", end_command))
    app.add_handler(CommandHandler("send", send_command))  # Added /send command

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print("Polling...")
    # Run the bot
    app.run_polling(poll_interval=3)
