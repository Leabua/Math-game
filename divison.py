from integers import generate_integer
from random import randint


# need to work on this
def division(total: int, level: int):
    score = 0
    for _ in range(total):
        try:
            # x * y = z therefore z / x = y
            if level == 1:
                x, y = randint(0, 6), randint(0, 6)
            elif level == 2:
                x, y = randint(0, 12), randint(0, 12)
            else:
                x, y = generate_integer(1), generate_integer(2)

            z = x * y

            for _ in range(3):
                try:
                    ans = int(input(f"{z} ÷ {x} = "))
                    if ans == y:
                        score += 1
                        break
                    else:
                        print("Wrong")
                        raise ValueError
                except ValueError:
                    pass

            else:
                print(f"{z} ÷ {x} = {y}")

        except ValueError:
            pass

    return score
