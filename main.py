# libraries
import random
import sys
import cowsay as cow

# modes
from main_modes.add import add
from main_modes.minus import minus
from main_modes.multiplication import multiply
from main_modes.divison import division

# utilities
import utilities.math_stats as s
from utilities.game_logic import get_name
from utilities.game_logic import total
from utilities.game_logic import get_level
from utilities.game_logic import get_mode
from utilities.game_logic import motivation

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

        if score is None:
            sys.exit("Score of type None.")
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


# this does a lot of the "routing".
# Could likely be simplified with a list and two if statements for the mode variables.
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

            motivation(name)

            if sign in ["addition", "+", "1"]:
                return add(mode, total, level)
            elif sign in ["subtraction", "-", "2"]:
                return minus(mode, total, level)
            elif sign in ["multiplication", "x", "*", "3"]:
                return multiply(mode, total, level)
            elif sign in ["division", "÷", "/", "4"]:
                return division(mode, total, level)
            else:
                print("Please enter +, -, x or /")

        except ValueError:
            print("Please enter +, -, x or /.")

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
