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
        "There’s a species of jellyfish that is biologically immortal; it can revert back to its juvenile form indefinitely.",
    "Wolves in a pack will howl in harmony rather than unison to avoid sounding like one animal to outsiders.",
    "The deepest part of the ocean is about 36,000 feet deep, deeper than Mount Everest is tall.",
    "Bees have five eyes: two large compound eyes and three smaller ocelli eyes.",
    "If you shuffled a deck of cards thoroughly, there’s a near 100% chance the exact order of the cards has never been seen before in history.",
    "The human nose and ears continue growing throughout a person’s entire life.",
    "Dragonflies have near 360-degree vision.",
    "A jiffy is an actual unit of time: 1/100th of a second.",
    "Spotted hyenas are more closely related to cats than to dogs.",
    "Sharks have been found living inside active volcanoes.",
    "Kangaroos can’t walk backward.",
    "Blue whales can eat up to 4 tons of krill each day.",
    "There’s a planet where it rains glass sideways due to 5,400 mph winds.",
    "Vikings used the bones of slain animals as part of their cooking process to add flavor to soups and stews.",
    "Some hummingbirds weigh less than a penny.",
    "Octopuses are known to decorate their lairs with rocks, shells, and shiny objects they find.",
    "The national animal of Scotland is the unicorn.",
    "The Great Wall of China is held together with sticky rice in some sections.",
    "In Japan, there’s an island populated solely by rabbits.",
    "Penguins propose to their mates with a pebble.",
    "A group of frogs is called an 'army.'",
    "Orcas (killer whales) are actually a species of dolphin.",
    "Beavers have transparent eyelids to see underwater while protecting their eyes.",
    "All clownfish are born male, but some turn female to lead their group.",
    "Snow leopards can’t roar like other big cats.",
    "You can tell the temperature by counting a cricket's chirps.",
    "A blob of toothpaste is called a 'nurdle.'",
    "Some metals are so reactive that they explode on contact with water.",
    "Humans are the only species known to blush.",
    "The longest hiccuping spree lasted 68 years.",
    "The tongue of a blue whale weighs as much as an elephant.",
    "Cows produce more milk when they listen to slow music.",
    "Ants can build rafts to survive floods.",
    "Humans and dolphins are the only species known to recognize themselves in mirrors.",
    "Peanuts are not nuts; they are legumes.",
    "The average cumulus cloud weighs roughly 1.1 million pounds.",
    "Camels have three eyelids to protect their eyes from blowing sand.",
    "A giraffe’s tongue is about 20 inches long and is dark blue to prevent sunburn.",
    "A shrimp’s heart is located in its head.",
    "In ancient Greece, throwing an apple at someone was considered a marriage proposal.",
    "A blue whale’s heart can weigh as much as a small car.",
    "Sea stars can regenerate lost arms, and in some species, a single arm can regenerate an entirely new starfish.",
    "Owls don’t have eyeballs; their eyes are tube-shaped, which is why they can’t move them.",
    "Tigers have striped skin, not just striped fur.",
    "Jellyfish evaporate in the sun because they’re 95% water.",
    "Honeybees can recognize human faces.",
    "A human can swim through the veins of a blue whale.",
    "Polar bears are nearly undetectable by infrared cameras due to their transparent fur.",
    "A chameleon’s tongue can be twice the length of its body.",
    "Pine trees have been found to live for over 5,000 years.",
    "The wood frog can hold its pee for up to 8 months.",
    "Crocodiles can’t stick their tongues out.",
    "Humans are bioluminescent, but the light is too faint for the human eye to detect.",
    "Rabbits can see behind them without moving their heads.",
    "Some octopuses punch fish for no reason other than annoyance.",
    "Cows can smell things up to six miles away.",
    "Butterflies remember their lives as caterpillars even after metamorphosis.",
    "Elephants are the only animals with four forward-facing knees.",
    "Kangaroos can't burp.",
    "There are more fake flamingos in the world than real ones.",
    "The Mantis shrimp can punch with the force of a bullet shot from a gun.",
    "The woodpecker's tongue wraps around its skull to protect its brain from injury.",
    "The platypus has no stomach; their esophagus goes straight to their intestines.",
    "Baby elephants suck their trunks for comfort, just like human babies suck their thumbs.",
    "A day on Mars is only about 40 minutes longer than a day on Earth.",
    "A starfish doesn’t have a brain, but it has a complex nervous system.",
    "The loudest sound produced by any animal is the blue whale's call, which can reach up to 188 decibels.",
    "Wolves can go for more than a week without eating.",
    "Koalas have fingerprints that are almost identical to human fingerprints.",
    "Sea otters have pockets in their skin where they can store food and tools.",
    "It takes a photon about 40,000 years to travel from the core of the sun to the surface, but only 8 minutes to reach Earth.",
    "The world's largest snow maze is located in Canada and spans over 30,000 square feet.",
    "Reindeer eyeballs turn blue in winter to help them see in the lower light levels.",
    "A queen termite can live up to 50 years and produce over 2,000 eggs per day.",
    "Bees can fly higher than Mount Everest.",
    "Sharks are older than trees. They have existed for more than 400 million years.",
    "A lion's roar can be heard from 5 miles away.",
    "The heart of a shrimp is located in its head.",
    "The fingerprints of a koala are so similar to a human's that they can taint crime scenes.",
    "Humans shed about 600,000 particles of skin every hour.",
    "The pistol shrimp can create a bubble so powerful that it produces light and sound hot enough to boil water.",
    "Some turtles can breathe through their butts.",
    "The word 'muscle' comes from a Latin term meaning 'little mouse,' which is what Ancient Romans thought muscles looked like.",
    "The average human body contains enough sulfur to kill all the fleas on an average dog.",
    "There's a species of ant, known as the 'zombie ant,' that is infected by a fungus, causing it to climb and die in a strategic place, helping spread the fungus further.",
    "You can find 13 muscles in the human ear alone.",
    "Dogs’ sense of smell is so powerful that they can detect medical problems, such as cancer and diabetes."
]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome! I can provide you with information about your Telegram account, /info Click here to know the information about your account. You can even play games with the bot, /games click here to play games.")

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
        ("📝 Fun Fact", "fun_fact"),  # Add FunFact button here
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
        send_fun_fact(call.message)  # Handle FunFact selection

def send_fun_fact(message):
    fact = random.choice(fun_facts)  # Select a random fun fact
    bot.reply_to(message, f"🧐 Fun Fact: {fact}")

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
