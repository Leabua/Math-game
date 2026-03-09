from integers import generate_integer


def add(total: int, level: int):
    score = 0
    for _ in range(total):
        try:
            x, y = generate_integer(level), generate_integer(level)

            for _ in range(3):
                try:
                    ans = int(input(f"{x} + {y} = "))
                    if ans == x + y:
                        score += 1
                        break
                    else:
                        print("Wrong")
                        raise ValueError
                except ValueError:
                    pass

            else:
                print(f"Correct answer: {x} + {y} = {x + y}")

        except ValueError:
            pass

    return score
