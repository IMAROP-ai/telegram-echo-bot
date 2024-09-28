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
    "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old!",
    "Bananas are berries, but strawberries aren't!",
    "Wombat poop is cube-shaped.",
    "A day on Venus is longer than a year on Venus.",
    "Sharks have been around longer than trees.",
    "Octopuses have three hearts.",
    "A single strand of spider silk is thinner than a human hair, but also five times stronger than steel of the same thickness.",
    "There are more stars in the universe than grains of sand on all the Earth's beaches.",
    "Elephants are the only animals that can’t jump.",
    "A group of flamingos is called a 'flamboyance.'",
    "Sloths can hold their breath longer than dolphins can.",
    "The Eiffel Tower can be 15 cm taller during the summer due to the expansion of metal in heat.",
    "Koalas sleep up to 22 hours a day.",
    "Butterflies taste with their feet.",
    "Ostriches can run faster than horses.",
    "Polar bears have black skin under their white fur.",
    "It rains diamonds on Jupiter and Saturn.",
    "Cows have best friends and get stressed when separated from them.",
    "Bananas glow blue under black light.",
    "Humans and giraffes have the same number of neck vertebrae – seven.",
    "Sea otters hold hands while sleeping to avoid drifting apart.",
    "Octopuses can taste with their arms.",
    "Squirrels plant thousands of trees every year simply by forgetting where they buried their acorns.",
    "Dolphins have names for each other.",
    "Caterpillars have 12 eyes.",
    "In Switzerland, it is illegal to own just one guinea pig because they get lonely.",
    "Rats laugh when tickled.",
    "Alfred Hitchcock was afraid of eggs.",
    "A cloud can weigh over a million pounds.",
    "A flea can accelerate faster than the Space Shuttle.",
    "Banging your head against a wall burns 150 calories an hour.",
    "Giraffes only need 5 to 30 minutes of sleep in a 24-hour period.",
    "A bolt of lightning contains enough energy to toast 100,000 slices of bread.",
    "Mosquitoes are attracted to the color blue twice as much as any other color.",
    "A snail can sleep for three years.",
    "Pineapples take about two years to grow.",
    "Turritopsis dohrnii, also known as the 'immortal jellyfish,' can revert back to its juvenile form after reaching adulthood, theoretically making it immortal.",
    "Humans share 50% of their DNA with bananas.",
    "A group of owls is called a 'parliament.'",
    "Starfish have no brains.",
    "The fingerprints of a koala are so indistinguishable from humans that they have on occasion been confused at crime scenes.",
    "Horses can sleep both lying down and standing up.",
    "There are more trees on Earth than stars in the Milky Way galaxy.",
    "The heart of a blue whale is so large that a human could swim through its arteries.",
    "A hippo's sweat is pink.",
    "Cheetahs can't roar, they meow like house cats.",
    "Humans are the only animals that blush.",
    "The moon has moonquakes.",
    "Alaska is the westernmost and easternmost state in the U.S.",
    "Tomatoes were once considered poisonous in Europe.",
    "There are more possible iterations of a game of chess than there are atoms in the observable universe.",
    "Goats have rectangular pupils.",
    "Water makes different pouring sounds depending on its temperature.",
    "A flock of crows is called a 'murder.'",
    "An octopus has nine brains.",
    "The hottest spot in the solar system is actually on Jupiter’s moon Io.",
    "Jellyfish are 95% water.",
    "A day on Mercury is twice as long as a year on Mercury.",
    "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.",
    "Cats have fewer toes on their back paws.",
    "Humans are the only animals with chins.",
    "If you fold a piece of paper 42 times, it would reach the moon.",
    "An eagle can kill a young deer and fly away with it.",
    "The Empire State Building has its own zip code.",
    "A flea can jump 350 times its body length.",
    "Sea cucumbers eat with their feet.",
    "A group of hedgehogs is called a 'prickle.'",
    "Jellyfish don’t have hearts.",
    "There are more bacteria in a human mouth than there are people in the world.",
    "The first oranges weren’t orange; they were green.",
    "Cows can walk upstairs, but they can’t walk down.",
    "Bats always turn left when exiting a cave.",
    "Ants never sleep.",
    "Wombats have backward-facing pouches.",
    "A group of porcupines is called a 'prickle.'",
    "Sharks are the only fish that can blink with both eyes.",
    "The average human will spend about six months of their life waiting for red lights to turn green.",
    "You can hear a blue whale’s heartbeat from over 2 miles away.",
    "In Japan, letting a sumo wrestler make your baby cry is considered good luck.",
    "Some fish cough.",
    "Tigers’ skin is striped, just like their fur.",
    "Bubble wrap was originally intended to be wallpaper.",
    "Cleopatra lived closer in time to the moon landing than to the construction of the Great Pyramid of Giza.",
    "Vending machines are twice as likely to kill you as a shark is.",
    "Bees sometimes sting other bees.",
    "Avocados are berries.",
    "The inventor of the frisbee was turned into a frisbee after he died.",
    "Dogs' sense of smell is 40 times better than humans'.",
    "A group of pandas is called an 'embarrassment.'",
    "The letter 'E' is the most common letter in the English language, appearing in 11% of all words.",
    "In France, it’s illegal to name a pig 'Napoleon.'",
    "Rabbits can’t vomit.",
    "Lobsters communicate by peeing at each other.",
    "The largest snowflake ever recorded was 15 inches wide.",
    "A group of jellyfish is called a 'smack.'",
    "Humans have about the same number of hair follicles as chimpanzees.",
    "A crocodile can’t stick its tongue out.",
    "Coca-Cola was the first soft drink in space.",
    "Your nose can remember 50,000 different scents.",
    "Sharks don't get cancer."
    "A snail has 14,000 teeth, and some species can even kill you with their venomous bite.",
    "The inventor of the microwave oven received only $2 for his discovery.",
    "The shortest commercial flight in the world lasts just 57 seconds.",
    "Butterflies can’t fly if they’re cold; their body temperature must be above 86°F to take off.",
    "The world’s oldest piece of chewing gum is over 9,000 years old.",
    "A bolt of lightning is five times hotter than the surface of the sun.",
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
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Contact Support", url="https://t.me/imarop"))  # Replace with your Telegram ID
    markup.add(InlineKeyboardButton("Info", callback_data="info"))
    markup.add(InlineKeyboardButton("Games", callback_data="games"))
    
    bot.reply_to(message, "👋 Welcome! You can contact support, get your account information, or play games.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "info":
        send_info(call.message)
    elif call.data == "games":
        show_games(call.message)

def send_info(message):
    user = message.from_user
    info = (
        "🆔 *Here is your account information* ℹ️ 😙\n\n"
        f"👤 *Username*: @{user.username or 'N/A'}\n"
        f"📛 *Full Name*: {user.first_name} {user.last_name or ''}\n"
        f"🔑 *Telegram ID*: `{user.id}`\n\n"
    )
    bot.reply_to(message, info, parse_mode='Markdown')

def show_games(message):
    markup = InlineKeyboardMarkup()
    games = [
        ("🎲 Guess the Number", "guess_number"),
        ("🧠 Hangman", "hangman"),
        ("🔢 Math Challenge", "math_challenge"),
        ("🧩 Fun Fact", "fun_fact")
    ]

    for game_name, game_callback in games:
        markup.add(InlineKeyboardButton(game_name, callback_data=game_callback))

    bot.reply_to(message, "Choose a mini-game to play or get a fun fact:", reply_markup=markup)

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
