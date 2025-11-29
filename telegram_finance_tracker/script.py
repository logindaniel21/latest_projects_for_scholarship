from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from datetime import datetime
import pytz

BOT_TOKEN = "8184456138:AAFl8W5GfWJlxdJiBYP3SEgHJh5YZUYRGXc"

LV_TZ = pytz.timezone("Europe/London")  # UK time


def change_balance(amount):
    with open("balance.txt", "r") as file:
        current = float(file.read().strip())

    new = current + amount

    with open("balance.txt", "w") as file:
        file.write(str(new))
    return new


def store_data(number, reasoning, left):
    now = datetime.now(LV_TZ)
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    with open("data.txt", "a") as f:
        if number > 0:
            f.write(f"{timestamp} | Daniel gained {number} bc of {reasoning} and has got {left} left\n\n")
        if number < 0:
            f.write(f"{timestamp} | Daniel has spent {abs(number)} on {reasoning} and has {left} left.\n\n")


def days_until_target():
    today = datetime.now(LV_TZ).date()
    target = datetime(2025, 12, 25).date()
    return (target - today).days


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text

    if message.lower() == "transactions":
        try:
            with open("data.txt", "r") as f:
                content = f.read()

            if not content.strip():
                await update.message.reply_text("Your transaction history is empty!")
            elif len(content) > 4000:
                for i in range(0, len(content), 4000):
                    await update.message.reply_text(content[i:i+4000])
            else:
                await update.message.reply_text(content)
        except Exception as e:
            await update.message.reply_text(f"Error reading file: {str(e)}")

    elif "," not in message:
        await update.message.reply_text("some bad syntax g")
    else:
        parts = message.split(",", 1)

        num = float(parts[0].strip())
        reason = str(parts[1].strip())

        balance = change_balance(num)

        await update.message.reply_text(
            f"You have {balance}GBP left\n\nYou also have an estimated {balance / days_until_target()} pounds to spend until christmas"
        )
        store_data(num, reason, balance)


# Main setup
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
