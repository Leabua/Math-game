# libraries
import random
import sys
import cowsay as cow
import pyfiglet as pyfig

# modules
from add import add
from level import get_level
from minus import minus
from multiplication import multiply
from divison import division
import math_stats as s

faces = (":)", ":p", ":0")

# best animals
cow_chars = [
    "trex",
    "cow",
    "dragon",
    "ghostbusters",
    "kitty",
    "meow",
    "milk",
    "stegosaurus",
    "turtle",
    "vader",
]


def main():
    stats = s.existing_stats()
    name = get_name()

    while True:
        level = get_level()
        t = total()
        score = sign(t, level, name)

        if score is None:
            sys.exit(1)

        stats = s.update_stats(stats, score, t)
        s.save_stats(stats)

        print(f"Score: {score}/{t} = {(score / t) * 100:.2f}%")
        s.display_stats(stats)

        if not play_again():  # that negative logic again
            char_func = getattr(cow, random.choice(cow_chars))
            char_func(f"Come back soon {random.choice(faces)}")
            break


def play_again():
    session = input("Want to play again? (yes/no) ").strip().lower()
    return session in ["yes", "y", ""]  # returns a boolean of true or false


def get_name():
    return input("Make a nickname? ")


def total():
    for _ in range(3):
        try:
            num = int(input("How many questions do you want? "))
            if num > 0:
                return num
            print("Please enter a positive number :) ")
        except ValueError:
            print("That is not a number. ")

    sys.exit("Too many invalid attempts :( ")


def sign(total, level, name):
    for _ in range(3):
        try:
            sign = (
                input(
                    "What do you want to practice?\n 1. Addition (+),\n 2. Subtraction (-),\n 3. Multiplication (*),\n 4. Division (/)\n"
                )
                .strip()
                .lower()
            )

            cool_name = pyfig.figlet_format(
                name, font=random.choice(pyfig.FigletFont.getFonts())
            )
            print(f"Let's go \n {cool_name}")

            if sign in ["addition", "+", "1"]:
                return add(total, level)
            elif sign in ["subtraction", "-", "2"]:
                return minus(total, level)
            elif sign in ["multiplication", "x", "*", "3"]:
                return multiply(total, level)
            elif sign in ["division", "÷", "/", "4"]:
                return division(total, level)
            else:
                print("Please enter +, -, x or /")

        except ValueError:
            print("Please enter +, -, x or /")

    print("Too many invalid attempts.")


if __name__ == "__main__":
    main()
