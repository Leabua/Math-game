from utilities.game_logic import generate_integer
from utilities.primes import is_prime


def primes_game(total: int, level: int):
    score = 0
    for _ in range(total):
        num = generate_integer(level)
        correct = is_prime(num)

        for _ in range(3):
            try:
                ans = input(f"Is {num} a prime number? (y/n): ").strip().lower()
                if ans not in ("y", "n"):
                    print("Please enter 'y' for yes or 'n' for no.")
                    raise ValueError

                user_yes = ans == "y"
                if user_yes == correct:
                    score += 1
                    break
                else:
                    print("Wrong!")
                    raise ValueError
            except ValueError:
                pass
        else:
            answer_str = "prime" if correct else "not prime"
            print(f"Correct answer: {num} is {answer_str}.")

    return score
