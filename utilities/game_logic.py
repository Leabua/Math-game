import pyfiglet as pyfig
from random import randint, choice
import sys


def generate_integer(level):
    if level == 1:
        number = randint(10 ** (level - 1) - 1, (10**level - 1))
    else:
        number = randint(10 ** (level - 1), (10**level - 1))

    return int(number)


def get_level():
    for _ in range(3):
        try:
            level = input("\nSelect difficulty (1-3): ")
            if level.isdigit() and 1 <= int(level) <= 3:
                print(f"You are on difficulty level {level}.")
                return int(level)

            raise ValueError

        except ValueError:
            print("Enter a number from 1 to 3.")


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


loading = "-------------------------------------"


def motivation(name):
    width = len(loading)
    motivation = "Let's go"

    cool_name = pyfig.figlet_format(name, font=choice(pyfig.FigletFont.getFonts()))

    if name == "":
        print(f"{loading}\n{motivation:^{width}}\n{loading}")
    else:
        print(f"{loading}\n{motivation:^{width}}\n{loading}\n{cool_name:^{width}}")
