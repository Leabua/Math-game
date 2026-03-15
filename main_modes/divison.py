from random import randint


# need to work on this
def division(mode: str, total: int, level: int):
    if mode == "x_mode":
        print("Solve for x.")

    score = 0

    for _ in range(total):
        # x * y = z therefore z / x = y
        if level == 1:
            x, y = randint(1, 6), randint(1, 6)
        elif level == 2:
            x, y = randint(1, 12), randint(1, 12)
        else:
            x, y = randint(1, 9), randint(10, 99)

        z = x * y

        for _ in range(3):
            try:
                if mode == "solve_mode":
                    ans = int(input(f"{z} ÷ {x} = "))
                    if ans == y:
                        score += 1
                        break
                elif mode == "x_mode":
                    ans = int(input(f"If {z} ÷ x = {y}, x is "))
                    if ans == x:
                        score += 1
                        break
                else:
                    print("Wrong")
                    raise ValueError

            except ValueError:
                pass

        else:
            if mode == "solve_mode":
                print(f"{z} ÷ {x} = {y}")
            if mode == "x_mode":
                print(f"{z} ÷ {x} = {y}. x is {x}")

    return score
