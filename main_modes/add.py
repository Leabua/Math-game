from utilities.game_logic import generate_integer


def add(mode: str, total: int, level: int):
    if mode == "x_mode":
        print("Solve for x.")
    score = 0
    for _ in range(total):
        x, y = generate_integer(level), generate_integer(level)
        z = x + y

        for _ in range(3):
            try:
                if mode == "solve_mode":
                    ans = int(input(f"{x} + {y} = "))
                    if ans == z:
                        score += 1
                        break

                elif mode == "x_mode":
                    ans = int(input(f"If x + {y} = {z}, x is "))
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
                print(f"Correct answer: {x} + {y} = {z}. x is {x}.")
            else:
                print(f"Correct answer: {x} + {y} = {z}.")

    return score
