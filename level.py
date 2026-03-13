def get_level():
    for _ in range(3):
        try:
            level = input("\nSelect difficulty (1-3): ")
            if level.isdigit() and 1 <= int(level) <= 3:
                print(f"You are on difficulty level {level}.")
                return int(level)

            raise ValueError

        except ValueError:
            print("Enter a number from 1 to 3.")
