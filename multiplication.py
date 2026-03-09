from integers import generate_integer
from random import randint


# need to work on this
def multiply(total: int, level: int):
    score = 0
    for _ in range(total):
        try:
            # this your standard 6 x 6
            if level == 1:
                x = randint(0, 6)
                y = randint(0, 6)
            # this is your standard timetable
            elif level == 2:
                x = randint(0, 12)
                y = randint(0, 12)
            # this should produce a 2 digit number x 1 - 12
            else:
                x, y = generate_integer(2), randint(0, 12)

            for _ in range(3):
                try:
                    ans = int(input(f"{x} x {y} = "))
                    if ans == x * y:
                        score += 1
                        break
                    else:
                        print("Wrong")
                        raise ValueError
                except ValueError:
                    pass

            else:
                print(f"{x} x {y} = {x * y}")

        except ValueError:
            pass

    return score
