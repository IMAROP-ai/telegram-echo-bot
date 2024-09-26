import os
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keep_alive import keep_alive  # Import the keep_alive function

keep_alive()  # Start the keep-alive server

bot = Bot(token=os.environ.get('token'))
dp = Dispatcher(bot)

# Define choices for Rock, Paper, Scissors
rock_paper_scissors_choices = ['Rock', 'Paper', 'Scissors']

# Emoji clues and their corresponding answers
emoji_quizzes = {
    '🍎🍏': 'APPLE',
    '🚀🌕': 'MOON',
    '🍕🍔': 'FOOD',
    '🐱🦁': 'CAT',
    '🌎🌍🌏': 'EARTH'
}

# Dictionary to keep track of each user's current game
current_games = {}

# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome! I can provide you with information about your Telegram account, /info Click here to know the information about your account. You can even play games with the bot, /games click here to play games")

# Info command
@bot.message_handler(commands=['info'])
def send_info(message):
    user = message.from_user
    premium_status = "Yes 💎" if user.is_premium else "No 🚫"

    info = (
        "🆔 *Here is your account information* ℹ️ 😙\n\n"
        f"👤 *Username*: @{user.username or 'N/A'}\n"
        f"📛 *Full Name*: {user.first_name} {user.last_name or ''}\n"
        f"💼 *Telegram Premium*: {premium_status}\n"
        f"🔑 *Telegram ID*: `{user.id}`\n\n"
        "For promotion or any issues - [@Imarop](https://t.me/imarop)"
    )
    bot.reply_to(message, info, parse_mode='Markdown')

# Mini-games command
@bot.message_handler(commands=['games'])
def show_games(message):
    markup = types.InlineKeyboardMarkup()
    games = [
        ("🎲 Guess the Number", "guess_number"),
        ("🧠 Hangman", "hangman"),
        ("🔢 Math Challenge", "math_challenge"),
        ("🧩 Emoji Game", "emoji_game"),
        ("🪨📄✂️ Rock, Paper, Scissors", "rock_paper_scissors"),
    ]

    for game_name, game_callback in games:
        markup.add(types.InlineKeyboardButton(game_name, callback_data=game_callback))

    bot.reply_to(message, "Choose a mini-game to play:", reply_markup=markup)

# Callback handler for mini-games
@bot.callback_query_handler(func=lambda call: True)
def handle_game_selection(call):
    user_id = call.from_user.id

    if call.data == "guess_number":
        current_games[user_id] = "guess_number"
        start_guess_game(call.message)
    elif call.data == "hangman":
        current_games[user_id] = "hangman"
        start_hangman(call.message)
    elif call.data == "math_challenge":
        current_games[user_id] = "math_challenge"
        start_math_challenge(call.message)
    elif call.data == "emoji_game":
        current_games[user_id] = "emoji_game"
        start_new_game(call.message)
    elif call.data == "rock_paper_scissors":
        current_games[user_id] = "rock_paper_scissors"
        start_rock_paper_scissors(call.message)
    elif call.data.startswith('rps_'):
        handle_rps_choice(call)

# Example game: Guess the Number
def start_guess_game(message):
    user_id = message.from_user.id
    number = random.randint(1, 10)
    msg = bot.reply_to(message, "🎲 I'm thinking of a number between 1 and 10. Can you guess it?")
    bot.register_next_step_handler(msg, check_guess, number)

def check_guess(message, number):
    user_id = message.from_user.id

    if current_games.get(user_id) != "guess_number":
        return
    
    try:
        guess = int(message.text)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Restart Guess the Number", callback_data="guess_number"))
        
        if guess == number:
            bot.reply_to(message, "🎉 Correct! You guessed it!", reply_markup=markup)
        else:
            bot.reply_to(message, f"❌ Wrong! The number was {number}. Try again.", reply_markup=markup)
    except ValueError:
        bot.reply_to(message, "Please send a number between 1 and 10.")

# Example game: Hangman
def start_hangman(message):
    user_id = message.from_user.id
    word = random.choice(["python", "telegram", "bot", "hangman", "game"])
    hidden_word = ["_" for _ in word]
    attempts = 6

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Restart Hangman", callback_data="hangman"))

    msg = bot.reply_to(message, "🎮 Let's play Hangman!\n" + " ".join(hidden_word), reply_markup=markup)
    bot.register_next_step_handler(msg, play_hangman, word, hidden_word, attempts)

def play_hangman(message, word, hidden_word, attempts):
    user_id = message.from_user.id

    if current_games.get(user_id) != "hangman":
        return

    guess = message.text.lower()

    if len(guess) != 1 or not guess.isalpha():
        msg = bot.reply_to(message, "Please guess a single letter.")
        bot.register_next_step_handler(msg, play_hangman, word, hidden_word, attempts)
        return

    if guess in word:
        for i, letter in enumerate(word):
            if letter == guess:
                hidden_word[i] = guess
        if "_" not in hidden_word:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Restart Hangman", callback_data="hangman"))
            bot.reply_to(message, f"🎉 Congratulations! You've guessed the word: {''.join(hidden_word)}", reply_markup=markup)
        else:
            msg = bot.reply_to(message, " ".join(hidden_word))
            bot.register_next_step_handler(msg, play_hangman, word, hidden_word, attempts)
    else:
        attempts -= 1
        if attempts == 0:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Restart Hangman", callback_data="hangman"))
            bot.reply_to(message, f"❌ Game Over! The word was '{word}'.", reply_markup=markup)
        else:
            msg = bot.reply_to(message, f"Incorrect! You have {attempts} attempts left.\n" + " ".join(hidden_word))
            bot.register_next_step_handler(msg, play_hangman, word, hidden_word, attempts)

# Math Challenge Game
def start_math_challenge(message):
    user_id = message.from_user.id

    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(['+', '-', '*'])
    
    if operator == '+':
        correct_answer = num1 + num2
    elif operator == '-':
        correct_answer = num1 - num2
    elif operator == '*':
        correct_answer = num1 * num2
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Restart Math Challenge", callback_data="math_challenge"))

    msg = bot.reply_to(message, f"🔢 Solve this: {num1} {operator} {num2} = ?", reply_markup=markup)
    bot.register_next_step_handler(msg, check_math_answer, correct_answer)

def check_math_answer(message, correct_answer):
    user_id = message.from_user.id

    if current_games.get(user_id) != "math_challenge":
        return

    try:
        user_answer = int(message.text)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Restart Math Challenge", callback_data="math_challenge"))
        
        if user_answer == correct_answer:
            bot.reply_to(message, "🎉 Correct! Well done!", reply_markup=markup)
        else:
            bot.reply_to(message, f"❌ Incorrect! The correct answer was {correct_answer}. Try again.", reply_markup=markup)
    except ValueError:
        bot.reply_to(message, "Please enter a valid number.")

# Emoji Game
games = {}

def start_new_game(chat_id):
    emoji, answer = random.choice(list(quizzes.items()))
    games[chat_id] = {
        'emoji': emoji,
        'answer': answer,
        'attempts': 3
    }
    bot.send_message(chat_id, f"Guess the word based on this emoji clue: {emoji}")
    bot.send_message(chat_id, "You have 3 attempts.")

@bot.message_handler(commands=['start'])
def start_game(message):
    chat_id = message.chat.id
    start_new_game(chat_id)

@bot.message_handler(func=lambda message: message.text.isalpha())
def handle_guess(message):
    chat_id = message.chat.id
    if chat_id in games:
        guess = message.text.upper()
        game = games[chat_id]
        answer = game['answer']
        attempts = game['attempts']

        if guess == answer:
            bot.send_message(chat_id, f"Congratulations! You guessed correctly. The word was {answer}.")
            del games[chat_id]
        else:
            game['attempts'] -= 1
            if game['attempts'] <= 0:
                bot.send_message(chat_id, f"Game over! The word was {answer}.")
                del games[chat_id]
            else:
                bot.send_message(chat_id, f"Incorrect! Try again. Attempts left: {game['attempts']}")

# Start polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
