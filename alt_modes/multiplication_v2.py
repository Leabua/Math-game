from utilities.game_logic import generate_integer
from random import randint


# need to work on this
def multiply_v2(total: int, level: int):
    print("What should x be?")
    score = 0
    for _ in range(total):
        # this your standard 6 x 6
        if level == 1:
            x = randint(1, 6)
            y = randint(1, 6)
        # this is your standard timetable
        elif level == 2:
            x = randint(1, 12)
            y = randint(1, 12)
        # this should produce a 2 digit number x 1 - 12
        else:
            x, y = generate_integer(2), randint(1, 12)

        z = x * y

        for _ in range(3):
            try:
                ans = int(input(f"If [x] x {y} = {z}, x is "))
                if ans == x:
                    score += 1
                    break
                else:
                    print("Wrong")
                    raise ValueError
            except ValueError:
                pass

        else:
            print(f"{x} x {y} = {z}. x is {x}.")

    return score
