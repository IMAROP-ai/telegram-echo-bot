import os
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keep_alive import keep_alive  # Import the keep_alive function

keep_alive()  # Start the keep-alive server

bot = Bot(token=os.environ.get('token'))
dp = Dispatcher(bot)
current_games = {}

# Welcome command
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("👋 Welcome! I can provide you with information about your Telegram account, /info Click here to know the information about your account. You can even play games with the bot, /games click here to play games")

# Info command
@dp.message_handler(commands=['info'])
async def send_info(message: types.Message):
    user = message.from_user
    info = (
        "🆔 *Here is your account information* ℹ️ 😙\n\n"
        f"👤 *Username*: @{user.username or 'N/A'}\n"
        f"📛 *Full Name*: {user.first_name} {user.last_name or ''}\n"
        f"🔑 *Telegram ID*: `{user.id}`\n\n"
        "For promotion or any issues - [@Imarop](https://t.me/imarop)"
    )
    await message.reply(info, parse_mode='Markdown')

# Games command
@dp.message_handler(commands=['games'])
async def show_games(message: types.Message):
    markup = InlineKeyboardMarkup()
    games = [
        ("🎲 Guess the Number", "guess_number"),
        ("🧠 Hangman", "hangman"),
        ("🔢 Math Challenge", "math_challenge"),
    ]
    for game_name, game_callback in games:
        markup.add(InlineKeyboardButton(game_name, callback_data=game_callback))
    await message.reply("Choose a mini-game to play:", reply_markup=markup)

# Handle game selection
@dp.callback_query_handler(lambda call: True)
async def handle_game_selection(call: types.CallbackQuery):
    user_id = call.from_user.id
    if call.data == "guess_number":
        current_games[user_id] = "guess_number"
        await start_guess_game(call.message)
    elif call.data == "hangman":
        current_games[user_id] = "hangman"
        await start_hangman(call.message)
    elif call.data == "math_challenge":
        current_games[user_id] = "math_challenge"
        await start_math_challenge(call.message)

# Guess the Number game
async def start_guess_game(message: types.Message):
    number = random.randint(1, 10)
    msg = await message.reply("🎲 I'm thinking of a number between 1 and 10. Can you guess it?")
    dp.register_message_handler(lambda m: check_guess(m, number), lambda m: True)

async def check_guess(message: types.Message, number: int):
    try:
        guess = int(message.text)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Restart Guess the Number", callback_data="guess_number"))
        if guess == number:
            await message.reply("🎉 Correct! You guessed it!", reply_markup=markup)
        else:
            await message.reply(f"❌ Wrong! The number was {number}. Try again.", reply_markup=markup)
    except ValueError:
        await message.reply("Please send a number between 1 and 10.")

# Hangman game
async def start_hangman(message: types.Message):
    word = random.choice(["python", "telegram", "bot", "hangman", "game"])
    hidden_word = ["_" for _ in word]
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Restart Hangman", callback_data="hangman"))
    msg = await message.reply("🎮 Let's play Hangman!\n" + " ".join(hidden_word), reply_markup=markup)
    dp.register_message_handler(lambda m: play_hangman(m, word, hidden_word, 6), lambda m: True)

async def play_hangman(message: types.Message, word: str, hidden_word: list, attempts: int):
    guess = message.text.lower()
    if len(guess) != 1 or not guess.isalpha():
        msg = await message.reply("Please guess a single letter.")
        dp.register_message_handler(lambda m: play_hangman(m, word, hidden_word, attempts), lambda m: True)
        return

    if guess in word:
        for i, letter in enumerate(word):
            if letter == guess:
                hidden_word[i] = guess
        if "_" not in hidden_word:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("Restart Hangman", callback_data="hangman"))
            await message.reply(f"🎉 Congratulations! You've guessed the word: {''.join(hidden_word)}", reply_markup=markup)
        else:
            msg = await message.reply(" ".join(hidden_word))
            dp.register_message_handler(lambda m: play_hangman(m, word, hidden_word, attempts), lambda m: True)
    else:
        attempts -= 1
        if attempts == 0:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("Restart Hangman", callback_data="hangman"))
            await message.reply(f"❌ Game Over! The word was '{word}'.", reply_markup=markup)
        else:
            msg = await message.reply(f"Incorrect! You have {attempts} attempts left.\n" + " ".join(hidden_word))
            dp.register_message_handler(lambda m: play_hangman(m, word, hidden_word, attempts), lambda m: True)

# Math Challenge game
async def start_math_challenge(message: types.Message):
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(['+', '-', '*'])
    correct_answer = eval(f"{num1} {operator} {num2}")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Restart Math Challenge", callback_data="math_challenge"))
    msg = await message.reply(f"🔢 Solve this: {num1} {operator} {num2} = ?", reply_markup=markup)
    dp.register_message_handler(lambda m: check_math_answer(m, correct_answer), lambda m: True)

async def check_math_answer(message: types.Message, correct_answer: int):
    try:
        user_answer = int(message.text)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Restart Math Challenge", callback_data="math_challenge"))
        if user_answer == correct_answer:
            await message.reply("🎉 Correct! Well done!", reply_markup=markup)
        else:
            await message.reply(f"❌ Incorrect! The correct answer was {correct_answer}. Try again.", reply_markup=markup)
    except ValueError:
        await message.reply("Please enter a valid number.")

# Start polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
