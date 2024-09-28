import os
import random
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from keep_alive import keep_alive  # Import the keep_alive function

# Keep the bot alive
keep_alive()

# Use environment variable for token
API_TOKEN = os.environ.get('token')  # Your bot token
bot = telebot.TeleBot(API_TOKEN)

current_games = {}

# List of fun facts
fun_facts = [
    "Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3000 years old and still edible!",
    "Bananas are berries, but strawberries aren't!",
    "Octopuses have three hearts and blue blood!",
    "A group of flamingos is called a 'flamboyance.'",
    "Wombat poop is cube-shaped!"
]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Fun Fact", callback_data="fun_fact"))
    bot.reply_to(message, "👋 Welcome! I can provide you with information about your Telegram account, /info Click here to know the information about your account. You can even play games with the bot, /games click here to play games.", reply_markup=markup)

# Info command
@bot.message_handler(commands=['info'])
def send_info(message):
    user = message.from_user
    info = (
        "🆔 *Here is your account information* ℹ️ 😙\n\n"
        f"👤 *Username*: @{user.username or 'N/A'}\n"
        f"📛 *Full Name*: {user.first_name} {user.last_name or ''}\n"
        f"🔑 *Telegram ID*: `{user.id}`\n\n"
        
    )
    bot.reply_to(message, info, parse_mode='Markdown')

@bot.message_handler(commands=['games'])
def show_games(message):
    markup = InlineKeyboardMarkup()
    games = [
        ("🎲 Guess the Number", "guess_number"),
        ("🧠 Hangman", "hangman"),
        ("🔢 Math Challenge", "math_challenge"),
    ]

    for game_name, game_callback in games:
        markup.add(InlineKeyboardButton(game_name, callback_data=game_callback))

    bot.reply_to(message, "Choose a mini-game to play:", reply_markup=markup)

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
    elif call.data == "fun_fact":
        send_fun_fact(call.message)

def send_fun_fact(message):
    fact = random.choice(fun_facts)
    bot.reply_to(message, fact)

def start_guess_game(message):
    number = random.randint(1, 10)
    msg = bot.reply_to(message, "🎲 I'm thinking of a number between 1 and 10. Can you guess it?")
    bot.register_next_step_handler(msg, check_guess, number)

def check_guess(message, number):
    try:
        guess = int(message.text)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Restart Guess the Number", callback_data="guess_number"))
        if guess == number:
            bot.reply_to(message, "🎉 Correct! You guessed it!", reply_markup=markup)
        else:
            bot.reply_to(message, f"❌ Wrong! The number was {number}. Try again.", reply_markup=markup)
    except ValueError:
        bot.reply_to(message, "Please send a number between 1 and 10.")

def start_hangman(message):
    word = random.choice(["python", "telegram", "bot", "hangman", "game"])
    hidden_word = ["_" for _ in word]
    attempts = 6

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Restart Hangman", callback_data="hangman"))

    msg = bot.reply_to(message, "🎮 Let's play Hangman!\n" + " ".join(hidden_word), reply_markup=markup)
    bot.register_next_step_handler(msg, play_hangman, word, hidden_word, attempts)

def play_hangman(message, word, hidden_word, attempts):
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
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("Restart Hangman", callback_data="hangman"))
            bot.reply_to(message, f"🎉 Congratulations! You've guessed the word: {''.join(hidden_word)}", reply_markup=markup)
        else:
            msg = bot.reply_to(message, " ".join(hidden_word))
            bot.register_next_step_handler(msg, play_hangman, word, hidden_word, attempts)
    else:
        attempts -= 1
        if attempts == 0:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("Restart Hangman", callback_data="hangman"))
            bot.reply_to(message, f"❌ Game Over! The word was '{word}'.", reply_markup=markup)
        else:
            msg = bot.reply_to(message, f"Incorrect! You have {attempts} attempts left.\n" + " ".join(hidden_word))
            bot.register_next_step_handler(msg, play_hangman, word, hidden_word, attempts)

def start_math_challenge(message):
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(['+', '-', '*'])

    if operator == '+':
        correct_answer = num1 + num2
    elif operator == '-':
        correct_answer = num1 - num2
    elif operator == '*':
        correct_answer = num1 * num2

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Restart Math Challenge", callback_data="math_challenge"))

    msg = bot.reply_to(message, f"🔢 Solve this: {num1} {operator} {num2} = ?", reply_markup=markup)
    bot.register_next_step_handler(msg, check_math_answer, correct_answer)

def check_math_answer(message, correct_answer):
    try:
        user_answer = int(message.text)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Restart Math Challenge", callback_data="math_challenge"))
        if user_answer == correct_answer:
            bot.reply_to(message, "🎉 Correct! Well done!", reply_markup=markup)
        else:
            bot.reply_to(message, f"❌ Incorrect! The correct answer was {correct_answer}. Try again.", reply_markup=markup)
    except ValueError:
        bot.reply_to(message, "Please enter a valid number.")

# Run the bot
try:
    bot.polling(none_stop=True)
except Exception as e:
    print(f"Error occurred: {e}")
