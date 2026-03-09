from random import randint


def generate_integer(level):
    if level == 1:
        number = randint(10 ** (level - 1) - 1, (10**level - 1))
    else:
        number = randint(10 ** (level - 1), (10**level - 1))

    return int(number)
