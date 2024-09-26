from aiogram import Bot, Dispatcher, executor, types
import os
import random
from keep_alive import keep_alive

keep_alive()

bot = Bot(token=os.environ.get('token'))
dp = Dispatcher(bot)

current_question = None  # To keep track of the current question

def generate_question():
    """Generate a simple math question and return the question string and answer."""
    num1 = random.randint(1, 10)  # Random number between 1 and 10
    num2 = random.randint(1, 10)  # Random number between 1 and 10
    operation = random.choice(['+', '-'])  # Randomly choose addition or subtraction

    if operation == '+':
        answer = num1 + num2
        question = f"What is {num1} + {num2}?"
    else:
        answer = num1 - num2
        question = f"What is {num1} - {num2}?"

    return question, answer

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.reply("Hello! I'm Gunther Bot. Let's play a math game! Type /quiz to start.")

@dp.message_handler(commands=['quiz'])
async def quiz(message: types.Message):
    global current_question
    current_question = generate_question()  # Generate a new question
    await message.reply(current_question[0])  # Send the question

@dp.message_handler()
async def answer_question(message: types.Message):
    global current_question
    if current_question:
        try:
            user_answer = int(message.text)
            if user_answer == current_question[1]:
                await message.reply("Correct! 🎉 Type /quiz to play again.")
            else:
                await message.reply("Wrong answer! Try again or type /quiz for a new question.")
        except ValueError:
            await message.reply("Please send a valid number as your answer.")
    else:
        await message.reply("Type /quiz to start the game.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
