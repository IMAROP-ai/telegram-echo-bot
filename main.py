from aiogram import Bot, Dispatcher, executor, types
import os
import random
from keep_alive import keep_alive
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from telethon import TelegramClient

# Initialize the bot and dispatcher
keep_alive()

API_ID = '25287291'  # Your API ID
API_HASH = '4f986b87297a2daaf619a7acbdc1a872'  # Your API Hash
bot = Bot(token=os.environ.get('token'))
dp = Dispatcher(bot)

client = TelegramClient('anon', API_ID, API_HASH)

# Start the Telethon client asynchronously
async def on_startup(dp):
    await client.start()

# Global variables
current_question = None
current_game = None
word_list = ["python", "telegram", "bot", "hangman", "game"]  # Words for guessing game

def generate_question():
    """Generate a simple math question and return the question string and answer."""
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(['+', '-'])

    if operation == '+':
        answer = num1 + num2
        question = f"What is {num1} + {num2}?"
    else:
        answer = num1 - num2
        question = f"What is {num1} - {num2}?"

    return question, answer

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    # Create a welcome message with buttons
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🎮 Games"), KeyboardButton("🆔 My Info"))
    markup.add(KeyboardButton("🔍 Search User"))

    await message.reply("Welcome! I'm Gunther Bot. Choose an option below:", reply_markup=markup)

@dp.message_handler(lambda message: message.text == "🎮 Games")
async def games_menu(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Math Quiz"), KeyboardButton("Word Guessing Game"))
    markup.add(KeyboardButton("🔙 Back"))
    await message.reply("Select a game to play:", reply_markup=markup)

@dp.message_handler(lambda message: message.text == "🔙 Back")
async def back_to_main_menu(message: types.Message):
    await welcome(message)

@dp.message_handler(lambda message: message.text == "Math Quiz")
async def quiz(message: types.Message):
    global current_question
    current_question = generate_question()
    await message.reply(current_question[0])

@dp.message_handler(lambda message: message.text == "Word Guessing Game")
async def word_guessing_game(message: types.Message):
    global current_game
    current_game = random.choice(word_list)
    await message.reply("Guess the word! You have 3 attempts. Type your guess:")

@dp.message_handler(lambda message: message.text == "🆔 My Info")
async def user_info(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "No username"
    full_name = message.from_user.full_name

    info = f"User ID: {user_id}\nUsername: {username}\nFull Name: {full_name}"
    await message.reply(info)

@dp.message_handler(lambda message: message.text == "🔍 Search User")
async def search_user(message: types.Message):
    await message.reply("Enter the username you want to search (without @):")

@dp.message_handler(lambda message: not message.text.startswith('/') and message.text.isalnum())
async def handle_username(message: types.Message):
    username = message.text  # Remove the '@' character
    try:
        user = await client.get_entity(username)
        user_info = f"User ID: {user.id}\nUsername: @{user.username}\nFull Name: {user.first_name} {user.last_name or ''}"
        await message.reply(user_info)
    except Exception as e:
        await message.reply(f"User not found or error occurred: {e}")

@dp.message_handler()
async def answer_question(message: types.Message):
    global current_question
    global current_game

    if current_question:
        try:
            user_answer = int(message.text)
            if user_answer == current_question[1]:
                await message.reply("Correct! 🎉 Type /quiz to play again or choose another game.")
            else:
                await message.reply("Wrong answer! Try again or choose a game from the menu.")
        except ValueError:
            await message.reply("Please send a valid number as your answer.")
    elif current_game:
        if message.text.lower() == current_game:
            await message.reply(f"🎉 Congratulations! You've guessed the word: {current_game}.")
            current_game = None  # Reset current game
        else:
            await message.reply("❌ Incorrect! Try again.")
    else:
        await message.reply("Use the menu to select a game.")

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
