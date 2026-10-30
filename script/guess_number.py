from __future__ import annotations

import random


def play(low: int = 1, high: int = 100) -> int:
    """Run one game and return the number of valid attempts made."""
    if low > high:
        raise ValueError("low must not exceed high")

    target = random.randint(low, high)
    attempts = 0
    print(f"I'm thinking of an integer between {low} and {high}.")

    while True:
        try:
            guess = int(input("Your guess: ").strip())
        except ValueError:
            print("Please enter an integer.")
            continue

        if not low <= guess <= high:
            print(f"Out of range. Stay between {low} and {high}.")
            continue

        attempts += 1
        if guess < target:
            print("Too low.")
        elif guess > target:
            print("Too high.")
        else:
            print(f"Correct! Solved in {attempts} attempt(s).")
            return attempts


def main() -> None:
    print("--- Guess the Number ---")
    play(1, 100)

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
