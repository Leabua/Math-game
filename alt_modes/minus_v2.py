from utilities.game_logic import generate_integer


def minus_v2(total: int, level: int):
    print("What should x be?")
    score = 0
    for _ in range(total):
        x, y = generate_integer(level), generate_integer(level)
        z = x - y

        for _ in range(3):
            try:
                ans = int(input(f"If x - {y} = {z}, x is "))
                if ans == x:
                    score += 1
                    break
                else:
                    print("Wrong")
                    raise ValueError
            except ValueError:
                pass

        else:
            print(f"Correct answer: {x} - {y} = {z}. x is {x}.")

    return score
