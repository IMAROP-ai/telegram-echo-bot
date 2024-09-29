import os
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Get bot token from environment variable
TOKEN = os.environ.get('TOKEN')

# List of fun facts
fun_facts = [
    "The longest hiccuping spree lasted for 68 years.",
    "Elephants are the only animals that can't jump.",
    "Most lipstick contains fish scales.",
    "Octopuses have three hearts.",
    "Ants never sleep.",
    "An average person spends about one-third of their life sleeping.",
    "The tongue is the only muscle in the human body that is attached at just one end.",
    "The only food that doesn’t spoil is honey.",
    "Butterflies have their taste receptors in their feet.",
    "Rats and horses can’t vomit.",
]

# --- Command Handlers ---

async def start(update: Update, context) -> None:
    """Handles the /start command."""
    user = update.effective_user
    welcome_message = (
        f"Hello {user.first_name}, Welcome to TONZ!\n\n"
        "🌟 Start earning real money by mining Toncoin every second! Get 2 GH/s as a welcome gift 🎁.\n\n"
        "📝 Complete tasks, invite friends, and maximize your earnings 💰.\n\n"
        "🎯 Seize the chance to boost your income and aim for financial freedom with us 🎉!"
    )
    
    # Inline keyboard options
    keyboard = [
        [InlineKeyboardButton("💸 Start Mining", url='https://t.me/Ton_kombat_bot/app?startapp=5831493645')],
        [InlineKeyboardButton("📖 FAQ", callback_data='faq')],
        [InlineKeyboardButton("📞 Contact Support", url='http://t.me/CryptoStu2023')],
        [InlineKeyboardButton("🤔 Fun Fact", callback_data='fun_fact')]
    ]
    
    await update.message.reply_text(welcome_message, reply_markup=InlineKeyboardMarkup(keyboard))

async def help_command(update: Update, context) -> None:
    """Displays help information."""
    help_message = (
        "💡 *Help Information*\n\n"
        "1. Click 'Start Mining' to begin earning Toncoin.\n"
        "2. Click 'Fun Fact' for a random fact.\n"
        "3. For any issues, click 'Contact Support'."
    )
    await update.message.reply_text(help_message, parse_mode='Markdown')

async def faq(update: Update, context) -> None:
    """Displays Frequently Asked Questions."""
    faq_message = (
        "❓ *FAQ*\n\n"
        "1. *What is Toncoin?*\n"
        "Toncoin is a cryptocurrency you can earn by participating in this mining platform.\n\n"
        "2. *How do I earn?*\n"
        "You earn by completing tasks, inviting friends, and playing games.\n\n"
        "3. *How do I withdraw?*\n"
        "You can withdraw your earnings through your wallet at the airdrop."
    )
    await update.callback_query.message.reply_text(faq_message, parse_mode='Markdown')

async def fun_fact(update: Update, context) -> None:
    """Sends a random fun fact."""
    fact = random.choice(fun_facts)
    await update.callback_query.message.reply_text(f"🤔 *Fun Fact:*\n\n{fact}", parse_mode='Markdown')

async def contact_support(update: Update, context) -> None:
    """Provides contact support information."""
    await update.message.reply_text("📞 Contact support via @CryptoStu2023.")

# --- Error Handling ---

async def error_handler(update: Update, context) -> None:
    """Handles errors during bot updates."""
    logging.error(f"Exception occurred: {context.error}")
    if update.effective_message:
        await update.effective_message.reply_text("An error occurred. Please try again later.")

# --- Main Function ---

def main() -> None:
    """Starts the bot."""
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Callback query handlers for inline buttons
    app.add_handler(CallbackQueryHandler(faq, pattern='faq'))
    app.add_handler(CallbackQueryHandler(fun_fact, pattern='fun_fact'))

    # Message handler for text messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, contact_support))

    # Error handler
    app.add_error_handler(error_handler)

    # Start polling
    logging.info("Bot started polling...")
    app.run_polling()

if __name__ == '__main__':
    main()
