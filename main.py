# libraries
import random
import sys
import cowsay as cow
import pyfiglet as pyfig

# modules

# main_modes
from level import get_level
from main_modes.add import add
from main_modes.minus import minus
from main_modes.multiplication import multiply
from main_modes.divison import division

# alt_modes
from alt_modes.addition_v2 import add_v2
from alt_modes.minus_v2 import minus_v2
from alt_modes.multiplication_v2 import multiply_v2
from alt_modes.division_v2 import division_v2
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
]


def main():
    print(
        "At any point exit the game with Ctrl + C.\nGame stats will not be saved if you exit during a round.\n-------------------------------------"
    )
    stats = s.existing_stats()
    name = get_name()

    while True:
        t = total()
        mode = get_mode()
        difficulty = get_level()
        score = sign(mode, t, difficulty, name)

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
    return session in ["yes", "y", ""]  # returns a bool of true or false


def get_mode():
    for _ in range(3):
        try:
            mode = (
                input(
                    "\nChoose a mode.\n1. Solve mode, or\n2. Find x mode.\nYour choice: "
                )
                .strip()
                .lower()
            )
            if mode in ["1", "solve mode", "solve"]:
                return "solve_mode"
            elif mode in ["2", "find x mode", "x", "x mode"]:
                return "x_mode"
            else:
                print("Press 1 for solve or press 2 to find x?")
                raise ValueError
        except ValueError:
            pass


def get_name():
    return input("Make a nickname? ")


def total():
    for _ in range(3):
        try:
            num = int(input("\nHow many questions do you want?\nYour choice: "))
            if num > 0:
                return num
            print("Please enter a positive number :) ")
        except ValueError:
            print("That is not a number. ")

    sys.exit("Too many invalid attempts :( ")


# this does a lot of the "routing".
# Could likely be simplified with a list and two of statement for the mode variables.
def sign(mode, total, level, name):
    for _ in range(3):
        try:
            sign = (
                input(
                    "\nWhat do you want to practice?\n 1. Addition (+),\n 2. Subtraction (-),\n 3. Multiplication (*),\n 4. Division (/)\nYour choice: "
                )
                .strip()
                .lower()
            )

            cool_name = pyfig.figlet_format(
                name, font=random.choice(pyfig.FigletFont.getFonts())
            )
            print(f"\nLet's go \n {cool_name}\n-------------------------------------")

            if mode == "solve_mode":
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

            if mode == "x_mode":
                if sign in ["addition", "+", "1"]:
                    return add_v2(total, level)
                elif sign in ["subtraction", "-", "2"]:
                    return minus_v2(total, level)
                elif sign in ["multiplication", "x", "*", "3"]:
                    return multiply_v2(total, level)
                elif sign in ["division", "÷", "/", "4"]:
                    return division_v2(total, level)
                else:
                    print("Please enter +, -, x or /")

        except ValueError:
            print("Please enter +, -, x or /")

    print("Too many invalid attempts.")


if __name__ == "__main__":
    phrases = (
        "I guess we're done for now",
        "Okay that was a bit sudden. Bye, I guess.",
        "You probably need to go somewhere quicky. I understand.",
        "Game Terminated!!!",
    )
    try:
        main()
    except KeyboardInterrupt:
        # This catches Ctrl+C at any point in the game
        print(f"\n\n{random.choice(phrases)}")

        # Optional: Add a parting cow message here
        char_func = getattr(cow, random.choice(cow_chars))
        char_func(f"Goodbye! {random.choice(faces)}")

        sys.exit(0)
