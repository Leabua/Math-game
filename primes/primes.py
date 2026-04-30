import math

# location of the integer generator
from utilities.game_logic import generate_integer

# how to check if a number is a prime


def is_prime(n):
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    # Check from 5 up to sqrt(n), skipping even numbers
    for i in range(5, int(math.sqrt(n)) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True


numbers = []


def sequence(level: str):
    try:
        n = int(input("How many numbers do you want to try? "))
    except ValueError:
        print("Please enter a valid number.")
        return

    # generate x amount of numbers.
    numbers = []
    for _ in range(n):
        new_number = generate_integer(level)
        numbers.append(new_number)

    score = 0

    # Game Loop for the sequence
    for num in numbers:
        user_choice = input(f"Is {num} a prime number? (y/n): ").lower().strip()

        # Check against your is_prime function logic
        correct_answer = "y" if is_prime(num) else "n"

        if user_choice == correct_answer:
            print("Correct!")
            score += 1
        else:
            print(
                f"Wrong! {num} is {'prime' if correct_answer == 'y' else 'not prime'}."
            )

    print(f"\nSequence Complete! Your score: {score}/{n}")
    return score
