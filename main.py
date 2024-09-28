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
        "The mantis shrimp has the fastest punch in the animal kingdom, striking with the force of a bullet.",
"The Moon is moving away from the Earth at a rate of about 1.5 inches per year.",
"A baby puffin is called a 'puffling.'",
"Vultures can fly at altitudes of up to 37,000 feet.",
"Snakes can sense earthquakes up to five days before they happen.",
"Humans are the only species known to blush.",
"Octopuses have been known to escape from aquariums and return to the ocean.",
"The Eiffel Tower can be 15 cm taller during the summer due to heat expansion.",
"Sea cucumbers can expel their internal organs as a defense mechanism.",
"Cows have almost 360-degree panoramic vision.",
"Apples float in water because they are made up of 25% air.",
"A group of lemurs is called a 'conspiracy.'",
"The average human body contains enough sulfur to kill all the fleas on an average dog.",
"The longest recorded flight of a chicken is 13 seconds.",
"Goats have rectangular pupils which give them a wider field of vision.",
"Bees can recognize human faces and remember them.",
"Some fish can walk on land using their fins.",
"Peanuts aren’t actually nuts; they are legumes.",
"The heart of a shrimp is located in its head.",
"Dolphins have been known to protect humans from shark attacks.",
"The fastest muscle in the human body is the one that closes the eyelid.",
"Cows can produce more milk when they listen to soothing music.",
"Snails have 14,000 teeth and some can even kill you with their bite.",
"A dog's sense of smell is about 40 times better than humans'.",
"Honeybees can flap their wings up to 200 times per second.",
"The world’s largest pumpkin weighed over 2,600 pounds.",
"Sharks can live for five centuries or more.",
"Polar bears have black skin underneath their white fur to absorb heat from the sun.",
"The human eye can distinguish around 10 million different colors.",
"The largest animal in the world, the blue whale, weighs as much as 30 elephants.",
"Owls don’t have eyeballs; their eyes are tube-shaped, which allows them to see in the dark.",
"Bananas glow blue under ultraviolet light.",
"The longest recorded lifespan of a goldfish is 43 years.",
"Sea otters hold hands when they sleep to prevent drifting apart.",
"Almonds are a member of the peach family.",
"The first computer was invented in the 1940s and took up an entire room.",
"The Nile crocodile’s bite is three times stronger than a lion’s.",
"A kangaroo can’t hop unless its tail is touching the ground.",
"The world’s oldest piece of chewing gum is over 9,000 years old.",
"Octopuses can taste with their skin.",
"The fear of beards is called 'pogonophobia.'",
"The Great Wall of China is over 13,000 miles long.",
"A sneeze can travel up to 100 miles per hour.",
"Camels have three sets of eyelids to protect their eyes from sand.",
"Your stomach gets a new lining every three to four days.",
"A group of hedgehogs is called a 'prickle.'",
"Octopuses have nine brains and blue blood.",
"Sharks can go into a trance when flipped upside down.",
"Sloths can take up to a month to digest a single meal.",
"The fingerprints of a koala are almost indistinguishable from humans'.",
"Penguins propose to their mates with a pebble.",
"Only female mosquitoes bite; they need protein to produce eggs.",
"Elephants are the only mammals that can’t jump.",
"The fingerprints of humans and koalas are so similar that they have been mistaken for each other in crime investigations.",
"The human brain generates more electrical impulses in a day than all the telephones in the world.",
"Some jellyfish are biologically immortal and can revert to a younger stage after reaching adulthood.",
"The only letter not appearing on the periodic table is the letter 'J.'",
"Sharks have been around longer than trees.",
"Orca whales are the largest members of the dolphin family.",
"A group of crows is called a 'murder.'",
"A cat’s whiskers are roughly the same width as its body, allowing them to gauge if they can fit through small spaces.",
"Some turtles can breathe through their butts.",
"An octopus can change color to match its surroundings in less than a second.",
"The average person will spend six months of their life waiting for red lights to turn green.",
"The Guinness World Record for the longest hiccups lasted for 68 years.",
"Octopuses can regrow lost arms.",
"The human body contains enough fat to make seven bars of soap.",
"Sea sponges have no brains, yet they are considered animals.",
"The oldest continuously inhabited city in the world is Damascus, Syria.",
"The heaviest onion ever grown weighed over 18 pounds.",
"The human body has over 600 muscles.",
"Bees are responsible for pollinating about one-third of the food we eat.",
"Cows can remember faces for years.",
"The light from the Sun takes about 8 minutes and 20 seconds to reach Earth.",
"Some frogs can be frozen and then thawed, and they will hop away as if nothing happened.",
"The world’s oldest piece of chewing gum is over 9,000 years old.",
"The average human blinks about 15-20 times per minute.",
"A cat’s purr can help heal bones and tissues.",
"Kangaroos can't walk backward.",
"The oldest living tree is over 4,800 years old.",
"Sea otters have a pouch in their armpit to store food.",
"The largest living structure on Earth is the Great Barrier Reef.",
"Dolphins can communicate with each other by whistling.",
"The average cloud weighs over a million pounds.",
"Cats have more bones in their bodies than humans do.",
"A bolt of lightning contains enough energy to toast 100,000 slices of bread.",
"Octopuses have copper-based blood, which gives it a blue color.",
"A sneeze can travel at speeds of up to 100 miles per hour.",
"Sharks are the only fish that can blink with both eyes.",
"The shortest war in history lasted for only 38 minutes between Britain and Zanzibar.",
"A group of jellyfish is called a 'smack.'",
"Slugs have four noses.",
"The blue whale is the loudest animal on Earth.",
"Sea otters wrap themselves in seaweed to keep from floating away while they sleep.",
"The sound of a tiger’s roar can be heard up to two miles away.",
"Butterflies can see ultraviolet light, which is invisible to the human eye.",
"A group of pandas is called an 'embarrassment.'",
"A lion’s roar can be heard from five miles away.",
"Goldfish have a memory span of at least three months.",
"A baby echidna is called a 'puggle.'",
"The average person spends about six years of their life dreaming.",
"Horses use facial expressions to communicate with each other.",
"The only letter not used in any of the U.S. state names is 'Q.'",
"The Earth’s core is as hot as the surface of the Sun.",
"An octopus has three hearts, two of which pump blood to its gills.",
"The world’s oldest piece of chewing gum is over 9,000 years old.",
"A group of flamingos is called a 'flamboyance.'",
"The fear of long words is called 'hippopotomonstrosesquippedaliophobia.'",
"Penguins have been known to propose with a pebble to their mates.",
"A blue whale’s tongue can weigh as much as an elephant.",
"Honey never spoils; it has been found in ancient Egyptian tombs still edible after thousands of years.",
"Humans share 99% of their DNA with chimpanzees.",
"The Guinness World Record for the longest fingernails is over 28 feet long.",
"Cats have over 20 muscles that control their ears.",
"Polar bears have black skin to absorb heat from the sun.",
"Apples float in water because they are 25% air.",
"A group of crows is called a 'murder.'",
"The largest living organism in the world is a fungus in Oregon.",
"An ostrich’s eye is bigger than its brain.",
"The Earth is not perfectly round; it is slightly flattened at the poles and bulging at the equator.",
"A chameleon’s tongue is twice the length of its body.",
"Sloths only defecate once a week and lose one-third of their body weight when they do.",
"The smell of freshly cut grass is actually a plant distress call.",
"Snakes don’t have eyelids, so they can’t blink.",
"A giraffe’s heart weighs about 25 pounds and is the size of a basketball.",
"Honeybees can recognize human faces.",
"The fingerprints of koalas are so similar to humans that they have been mistaken at crime scenes.",
"The longest flight of a chicken was 13 seconds.",
"The average human produces enough saliva in their lifetime to fill two swimming pools.",
"A tarantula can live for two years without food.",
"Sharks are immune to almost all known diseases.",
"The Great Wall of China is the longest man-made structure in the world, stretching over 13,000 miles.",
"The ostrich is the world’s largest bird and can run up to 45 miles per hour.",
"Hummingbirds weigh less than a penny and can flap their wings up to 80 times per second.",
"A group of parrots is called a 'pandemonium.'",
"Jellyfish have been around for over 600 million years.",
"A single strand of spaghetti is called a 'spaghetto.'",
"Octopuses are known to collect shiny objects and create collections in their dens.",
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
"The cigarette lighter was invented before the match.",
"A duck’s quack doesn’t echo, and no one knows why.",
"Women blink nearly twice as much as men.",
"Starfish don’t have brains.",
"The average person sheds around 600,000 particles of skin every hour.",
"A hummingbird’s heart beats over 1,200 times per minute.",
"A group of frogs is called an 'army.'",
"Giraffes have no vocal cords.",
"A crocodile can’t stick its tongue out.",
"A shrimp’s heart is in its head.",
"The average person has 100,000 to 150,000 strands of hair on their head.",
"Polar bear fur is not white; it’s transparent, and their skin is black.",
"The world's smallest frog is less than half an inch long.",
"Water makes up around 60% of the human body.",
"The smallest country in the world is Vatican City.",
"The shortest war in history was fought between Britain and Zanzibar in 1896, lasting just 38 minutes.",
"Sharks lay the largest eggs in the world.",
"The 'ZIP' in ZIP code stands for 'Zone Improvement Plan.'",
"Every minute, about 150 people are born.",
"The microwave was invented after a researcher walked by a radar tube and a chocolate bar melted in his pocket.",
"A sneeze travels at about 100 miles per hour.",
"Fingernails grow nearly four times faster than toenails.",
"Human bones are stronger than concrete.",
"The lifespan of a housefly is about 30 days.",
"Bananas are berries, while strawberries are not.",
"Cows have best friends.",
"A group of porcupines is called a 'prickle.'",
"Elephants can smell water up to 12 miles away.",
"Humans share 98.8% of their DNA with chimpanzees.",
"The electric chair was invented by a dentist.",
"A cow-bison hybrid is called a 'beefalo.'",
"Butterflies can’t fly if their body temperature is below 86 degrees Fahrenheit.",
"Polar bears can swim for days without stopping.",
"Dragonflies can fly up to 60 miles per hour.",
"The longest wedding veil was the same length as 63.5 football fields.",
"A cat’s whiskers are generally about the same width as its body.",
"Sharks are immune to almost all known diseases.",
"The fingerprints of koalas are almost indistinguishable from those of humans.",
"On average, your hair will grow about half an inch per month.",
"The brain is the fattiest organ in the body, made up of about 60% fat.",
"Kangaroos can’t walk backward.",
"Dolphins sleep with one eye open.",
"The longest recorded flight of a chicken is 13 seconds.",
"A group of jellyfish is called a 'smack.'",
"Arachnophobia is the fear of spiders.",
"Bananas are slightly radioactive.",
"Cows can go upstairs, but not downstairs.",
"The Eiffel Tower can grow by six inches in the summer.",
"Horses use facial expressions to communicate with each other.",
"Oysters can change gender depending on which is best for mating.",
"The heart of a blue whale weighs about as much as a car.",
"Sharks have been around for more than 400 million years.",
"Bees can fly higher than Mount Everest.",
"The first oranges weren’t orange—they were green.",
"The longest-living insect is the termite queen, which can live up to 50 years.",
"A snail can sleep for up to three years.",
"Slugs have four noses.",
"Elephants are capable of understanding pointing gestures.",
"A starfish can regenerate its arms.",
"A blue whale’s tongue weighs as much as an elephant.",
"A day on Venus lasts longer than a year on Venus.",
"A group of flamingos is called a 'flamboyance.'",
"The sound a camel makes is called 'nuzzing.'",
"The scientific name for a bison is 'Bison bison bison.'",
"Octopuses are capable of opening jars from the inside.",
"Sharks don't get cancer.",
"Hummingbirds are the only birds that can fly backward.",
"The human brain has the same consistency as tofu.",
"A group of parrots is called a 'pandemonium.'",
"The fear of long words is called 'hippopotomonstrosesquippedaliophobia.'",
"A lion’s roar can be heard from five miles away.",
"Some cats are allergic to humans.",
"The shortest commercial flight in the world lasts about 57 seconds.",
"The inventor of the frisbee was turned into a frisbee after he died.",
"Butterflies can remember things they learned as caterpillars.",
"The platypus doesn’t have a stomach.",
"Humans are the only animals that can blush.",
"Kangaroos can hop 25 feet in a single bound.",
"Some turtles can breathe through their butts.",
"The oldest known living land animal is a tortoise named Jonathan, born in 1832.",
"Dolphins have been seen giving each other names.",
"There are more fake flamingos in the world than real ones.",
"The shortest bone in the human body is in the ear.",
"A day on Mercury is longer than a year on Mercury.",
"Humans and dolphins are the only animals that have sex for pleasure.",
"Bees can recognize human faces.",
"Octopuses can change the color of their skin within milliseconds.",
"Flamingos are naturally white, but turn pink from eating shrimp.",
"Sea otters have a favorite rock they use to crack open shellfish.",
"The male seahorse is the one that gives birth to babies.",
"Jellyfish have been around for over 600 million years, predating dinosaurs.",
"Orca whales are actually dolphins.",
"Human teeth are just as strong as shark teeth.",
"Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old.",
"The average adult human has two to nine pounds of bacteria in their body.",
"A group of crows is called a 'murder.'",
"An eagle’s vision is about five times sharper than a human’s.",
"A narwhal’s tusk is actually a tooth.",
"The human nose can detect about one trillion different scents.",
"Elephants are the only mammals that can’t jump.",
"Octopuses can squeeze through any hole that is larger than their beak.",
"The fingerprints of koalas are almost identical to humans and have been confused at crime scenes.",
"Slugs have four noses.",
"Elephants are pregnant for nearly two years.",
"A housefly hums in the key of F.",
"The Statue of Liberty’s index finger is eight feet long.",
"Bees can communicate with each other by dancing.",
"A group of unicorns is called a 'blessing.'",
"Penguins can jump as high as six feet in the air.",
"Baby elephants suck their trunks for comfort, just like human babies suck their thumbs.",
"The fingerprints of koalas are so similar to humans that they can be confused at a crime scene.",
"Male seahorses carry and give birth to their young.",
"The average person walks the equivalent of five times around the world in their lifetime.",
"Dolphins can hear sounds underwater from up to 15 miles away.",
"The longest word in the English language is 189,819 letters long and refers to a protein.",
"A jiffy is an actual unit of time; it's 1/100th of a second.",
"Giraffes have the same number of neck vertebrae as humans.",
"The Earth weighs about 13.2 sextillion pounds.",
"The Great Wall of China is not visible from space without aid.",
"A group of flamingos is called a flamboyance.",
"Frogs can breathe through their skin.",
"A woodpecker’s tongue can wrap around its brain to cushion it during pecking.",
"The largest snowflake ever recorded was 15 inches wide.",
"Arachnophobia is the fear of spiders.",
"Ostriches can run faster than horses.",
"A shrimp’s heart is located in its head.",
"A day on Venus is longer than a year on Venus.",
"Some fish can walk on land.",
"Sharks have been around longer than trees.",
"A dragonfly’s lifespan is only 24 hours.",
"A group of hedgehogs is called a prickle.",
"The loudest sound ever recorded was the eruption of Krakatoa in 1883.",
"Owls are the only birds that can see the color blue.",
"The first oranges were not orange; they were green.",
"A group of frogs is called an army.",
"Some turtles can breathe through their butts.",
"A human sneeze can travel over 100 miles per hour.",
"Sloths can take up to a month to digest their food.",
"The fingerprints of a koala are so indistinguishable from humans that they have been confused at crime scenes.",
"The longest recorded flight of a chicken is 13 seconds.",
"Sharks are immune to almost all known diseases.",
"The fingerprints of koalas are almost indistinguishable from those of humans.",
"Sea otters use rocks to break open shellfish.",
"A single strand of spaghetti is called a spaghetto.",
"The unicorn is the national animal of Scotland.",
"Beavers can hold their breath underwater for up to 15 minutes.",
"Octopuses have blue blood because of a copper-based molecule called hemocyanin.",
"This bot is made my @IMAROP 😎 !! "
"The shortest commercial flight in the world is just 57 seconds long, between two Scottish islands.",
"A group of flamingos is called a 'flamboyance.'",
"An octopus has nine brains and three hearts.",
"Sharks are the only fish that can blink with both eyes.",
"The unicorn is the national animal of Scotland.",
"Bamboo can grow up to 35 inches in a single day.",
"Hot water freezes faster than cold water under certain conditions, known as the Mpemba effect.",
"Horses can't vomit.",
"Blue whales are the largest animals to have ever lived, even bigger than dinosaurs.",
"Butterflies can taste with their feet.",
"There are more stars in the universe than grains of sand on all of Earth’s beaches.",
"More people visit France than any other country in the world.",
"Hummingbirds are the only birds that can fly backwards.",
"The average cloud weighs over a million pounds.",
"The sound of ET walking in the movie 'E.T.' was made by someone squishing their hands in jelly.",
"A bolt of lightning contains enough energy to toast 100,000 slices of bread.",
"Potatoes were the first food to be grown in space.",
"Cleopatra lived closer in time to the first Moon landing than to the construction of the Great Pyramid of Giza.",
"Humans share 60% of their DNA with bananas.",
"The longest wedding veil was longer than 63 football fields.",
"Spiders can’t fly, but they can glide using silk threads to catch the wind.",
"Sloths only poop once a week, and it’s always on the ground.",
"Dolphins have names for each other and can recognize these names.",
"The Eiffel Tower grows by up to six inches in the summer because the metal expands in the heat.",
"Sharks don’t have bones; their skeletons are made of cartilage.",
"A day on Mercury lasts 1,408 hours.",
"Sea otters hold hands while sleeping to avoid drifting apart.",
"Cows produce more milk when they listen to slow music.",
"Every year, millions of trees grow because squirrels forget where they buried their nuts.",
"The average person spends six months of their life waiting for red lights to turn green.",
"There’s a species of jellyfish that is biologically immortal.",
"Vikings used the bones of slain animals to strengthen their swords.",
"Only male crickets chirp.",
"The world’s smallest reptile, Brookesia nana, is about the size of a sunflower seed.",
"A jellyfish is about 95% water.",
"An ostrich can run faster than a horse.",
"The longest recorded lifespan of a goldfish was 43 years.",
"Elephants are pregnant for almost two years.",
"At birth, a baby panda is smaller than a mouse.",
"The scent of fresh-cut grass is a plant’s way of signaling distress.",
"Lightning strikes the Earth about 100 times every second.",
"Bananas glow blue under black lights.",
"The world's deepest postbox is in Susami Bay, Japan, and is 33 feet underwater.",
"Koalas sleep up to 22 hours a day.",
"A snail can sleep for up to three years.",
"The scientific name for a western lowland gorilla is 'Gorilla gorilla gorilla.'",
"Humans are the only animals that blush.",
"Scorpions can survive up to a year without food.",
"The heart of a shrimp is located in its head.",
"Sharks have existed for over 400 million years.",
"On average, people spend about 90 days of their lives on the toilet.",
"An ant can lift 50 times its body weight.",
"The average person walks about 75,000 miles in their lifetime.",
"Octopuses have been observed using tools.",
"The average lifespan of a mosquito is just two weeks.",
"Water covers 71% of the Earth’s surface.",
"Dolphins sleep with one eye open.",
"Flamingos are born gray and turn pink due to their diet of shrimp and algae.",
"Bees can fly higher than Mount Everest.",
"Polar bears can overheat in temperatures as cold as 32°F.",
"Kangaroos can’t walk backward.",
"Jellyfish have been around for over 600 million years.",
"Goldfish can recognize their owners.",
"The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.",
"Owls can turn their heads 270 degrees.",
"The longest hiccuping spree lasted 68 years.",
"A hummingbird's wings can flap up to 80 times per second.",
"Bananas are curved because they grow towards the sun.",
"Some sea stars can regrow lost arms.",
"Honey never spoils; it has been found in Egyptian tombs still edible after thousands of years.",
"Cows have best friends and get stressed when they are separated.",
"Humans and giraffes have the same number of neck vertebrae—seven.",
"Koalas have fingerprints that are almost indistinguishable from human fingerprints.",
"Peanuts aren’t technically nuts; they’re legumes.",
"A cheetah can accelerate from 0 to 60 miles per hour in just 3 seconds.",
"The oldest living tree on Earth is over 4,800 years old.",
"The fingerprints of a koala are almost indistinguishable from those of a human.",
"Penguins can leap several feet in the air.",
"The human brain is about 75% water.",
"A group of hedgehogs is called a 'prickle.'",
"A bolt of lightning is five times hotter than the surface of the Sun.",
"The human body contains enough iron to make a 3-inch nail.",
"Apples are made of 25% air, which is why they float in water.",
"The dot over the lowercase 'i' and 'j' is called a 'tittle.'",
"Humans share 99% of their DNA with chimpanzees.",
"A crocodile can't stick its tongue out.",
"All pandas in the world are on loan from China.",
"The blue whale is the loudest animal on Earth, producing sounds up to 188 decibels.",
"A sneeze can travel at over 100 miles per hour.",
"Alaska is the only U.S. state that can be typed on one row of a keyboard.",
"The world's longest musical performance is currently taking place in Germany and is set to finish in 2640.",
"Polar bears have black skin under their white fur.",
"Honeybees can flap their wings 200 times per second.",
"The largest snowflake ever recorded was 15 inches wide.",
"A group of owls is called a 'parliament.'",
"Sharks are immune to almost all known diseases.",
"Frogs can’t vomit; if they need to rid their stomachs, they’ll eject it.",
"The average person breathes about 20,000 times a day.",
"Octopuses have copper-based blood, which gives them blue blood.",
"The fastest gust of wind ever recorded on Earth was 253 miles per hour.",
"The Sun is about 93 million miles away from Earth.",
"A blue whale’s heart can weigh as much as a car.",
"Dragonflies have been around for over 300 million years.",
"A snail can regenerate its eyes if they are damaged.",
"A baby octopus is about the size of a flea when it's born.",
"The brain operates on the same amount of power as a 10-watt lightbulb.",
"The world’s smallest bird is the bee hummingbird, which weighs less than a penny.",
"The Earth orbits the Sun at a speed of about 67,000 miles per hour.",
"A giraffe's tongue is about 20 inches long.",
"New York drifts about one inch farther from London each year.",
"The world's largest sandcastle was over 57 feet tall.",
"A single strand of hair can hold up to 3 ounces of weight.",
"Sea otters use rocks to crack open shellfish.",
"Hummingbirds weigh less than a nickel.",
"The human body has 206 bones.",
"Rabbits can see behind them without moving their heads.",
"Sharks have been around longer than trees.",
"The longest recorded flight of a chicken was 13 seconds.",
"Hummingbirds have the highest metabolism of any animal.",
"A snail’s mouth is no larger than the head of a pin, yet it can have over 25,000 teeth.",
"The shortest bone in the human body is located in the ear.",
"Some species of bamboo can grow up to 3 feet in 24 hours.",
"Beavers have transparent eyelids that allow them to see underwater.",
"The scientific name for the giant anteater is 'Myrmecophaga tridactyla,' which means 'ant-eating, three-fingered animal.'",
"The largest volcano in the solar system is Olympus Mons on Mars.",
"Sharks can live for five centuries or more.",
"The Earth experiences over 50,000 earthquakes each year.",
"Dolphins have been known to protect humans from sharks.",
"The fingerprints of a koala are so indistinguishable from humans that they can cause confusion at crime scenes.",
"Polar bears can swim for days at a time without stopping.",
"Owls have three eyelids: one for blinking, one for sleeping, and one for keeping their eyes clean.",
"The largest living structure on Earth is the Great Barrier Reef."
        "The inventor of the popsicle was only 11 years old.",
"Cows can sense the Earth's magnetic field and tend to align themselves with it when they graze.",
"A cockroach can live for up to a week without its head before it dies of starvation.",
"A group of kangaroos is called a mob.",
"One teaspoon of honey represents the life work of 12 bees.",
"Crocodiles can't chew their food; they swallow it whole.",
"Slugs have four noses.",
"The fingerprints of a dog are found on its nose.",
"Octopuses have blue blood due to copper-based molecules in their blood.",
"The longest recorded flight of a chicken is 13 seconds.",
"The speed of a computer mouse is measured in 'Mickeys.'",
"A hippo can run faster than a human on land.",
"In medieval times, animals could be put on trial for crimes.",
"Cats can't taste sweet things.",
"Tigers have antiseptic saliva that can help clean their wounds.",
"The human stomach gets a new lining every three to four days to prevent it from digesting itself.",
"Firefighters use wetting agents to make water wetter.",
"Honeybees can recognize individual human faces.",
"There's a species of fish that can climb trees.",
"A giraffe can clean its ears with its tongue, which is 20 inches long.",
"The largest living organism is a fungus in Oregon, covering over 2,385 acres.",
"Some lizards can squirt blood from their eyes as a defense mechanism.",
"The bat is the only mammal capable of true flight.",
"A day on the planet Uranus lasts 17 hours.",
"There are more chickens than people in the world.",
"The average person will walk the equivalent of five times around the world in their lifetime.",
"The wood frog can freeze its body and then thaw back to life.",
"The ancient Romans used powdered mouse brains as toothpaste.",
"An ostrich's eye is bigger than its brain.",
"The 'jiffy' is an actual unit of time: 1/100th of a second.",
"The Eiffel Tower can shrink by six inches during cold weather.",
"Mosquitoes are the deadliest animals in the world, responsible for more human deaths than sharks and snakes combined.",
"Your nose gets warmer when you lie.",
"Rats multiply so quickly that in just 18 months, two rats could produce over 1 million descendants.",
"In space, astronauts grow about 2 inches taller due to the absence of gravity compressing the spine.",
"Some sea cucumbers fight off predators by expelling their internal organs, which they later regenerate.",
"The Canary Islands are named after dogs, not birds. The Latin name 'Canaria' means island of the dogs.",
"A shrimp’s heart is located in its head.",
"Bananas are radioactive due to their potassium content, though not enough to be harmful.",
"Alfred Hitchcock had no belly button after surgery for an abdominal hernia.",
"Vending machines kill more people annually than sharks.",
"The 'M' in M&Ms stands for Mars and Murrie, the last names of the candy’s founders.",
"Scallops have up to 100 tiny eyes that detect motion and light.",
"The longest hiccuping spree lasted 68 years.",
"Male seahorses, not females, give birth to their offspring.",
"Pineapple works as a natural meat tenderizer.",
"Walt Disney was afraid of mice.",
"The tallest snowman ever built was over 122 feet tall.",
"The chance of finding a pearl in an oyster is roughly 1 in 12,000.",
"The largest desert in the world is Antarctica.",
"A baby spider is called a spiderling.",
"The name for the shape of Pringles is called a 'hyperbolic paraboloid.'",
"Jellyfish have been around for over 500 million years, predating dinosaurs.",
"The shortest war in history lasted just 38 to 45 minutes, between Britain and Zanzibar in 1896.",
"A day on Venus is longer than a year on Venus.",
"All polar bears are left-handed.",
"A flea can jump up to 200 times its body length.",
"An elephant’s trunk has around 40,000 muscles in it.",
"The tallest mountain known to mankind is on an asteroid called Vesta.",
"The dot over a lowercase 'i' and 'j' is called a 'tittle.'",
"The moon has moonquakes, similar to earthquakes on Earth.",
"The original London Bridge is now in Arizona.",
"Humans are the only animals with chins.",
"Pigeons can differentiate between paintings by Monet and Picasso.",
"A duck’s quack doesn’t echo, and nobody knows why.",
"Turtles can breathe through their butts.",
"The Guinness World Record for the longest hiccuping spree is held by Charles Osborne, who hiccupped for 68 years.",
"The Mantis shrimp has the world's fastest punch, accelerating at the speed of a bullet.",
"A cat’s purring can actually help heal bones and tissues.",
"The longest word in the English language is 189,819 letters long and refers to a type of protein.",
"Penguins have an organ above their eyes that converts seawater into fresh water.",
"Human bones are about five times stronger than steel.",
"There are more stars in the universe than grains of sand on Earth.",
"A 'buttload' is an actual unit of measurement for wine or whiskey, equating to about 126 gallons.",
"You’re more likely to get a computer virus from visiting religious sites than adult websites.",
"A crocodile can't stick its tongue out.",
"Humans are the only animals that enjoy spicy food.",
"A lion’s roar can be heard from five miles away.",
"The smell of freshly-cut grass is actually a plant distress signal.",
"Bananas are berries, but strawberries aren’t.",
"Snakes can help predict earthquakes by sensing tremors as far as five days before they happen.",
"There are more fake flamingos in the world than real ones.",
"Polar bears have black skin under their white fur.",
"In the Philippines, there is a species of giant clams that can grow to over 4 feet in diameter and weigh up to 500 pounds.",
"A group of ferrets is called a 'business.'",
"A shrimp can produce a sound wave that can break glass.",
"The inventor of the frisbee was turned into a frisbee after he died.",
"Some fish can walk on land.",
"The human body contains enough fat to make seven bars of soap.",
"The average person produces enough saliva in their lifetime to fill two swimming pools.",
"The national animal of Scotland is the unicorn.",
"Apples float in water because they are 25% air.",
"A blue whale’s tongue can weigh as much as an elephant.",
"The heart of a blue whale is so large a human could swim through its arteries.",
"If you keep a goldfish in a dark room, it will lose its color.",
"There are more people in California than in Canada.",
"Dragonflies have been around for 300 million years.",
"The hottest spot on the planet is in Libya, where the temperature reached 136 degrees Fahrenheit in 1922."
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
