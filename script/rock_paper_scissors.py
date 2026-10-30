"""Rock–Paper–Scissors against a uniform random opponent."""
from __future__ import annotations

import random

# Maps a choice to the choice it defeats: O(1) lookup instead of nested conditionals.
BEATS: dict[str, str] = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper",
}

ALIASES: dict[str, str] = {"r": "rock", "p": "paper", "s": "scissors"}


def decide(player: str, computer: str) -> str:
    """Return 'win', 'lose', or 'draw' from the player's perspective."""
    if player not in BEATS or computer not in BEATS:
        raise ValueError("choices must be rock, paper, or scissors")
    if player == computer:
        return "draw"
    return "win" if BEATS[player] == computer else "lose"


def normalize(raw: str) -> str | None:
    token = raw.strip().lower()
    token = ALIASES.get(token, token)
    return token if token in BEATS else None


def main() -> None:
    print("--- Rock, Paper, Scissors ---")
    score = {"win": 0, "lose": 0, "draw": 0}

    while True:
        raw = input("\nYour choice (rock/paper/scissors, or 'quit'): ")
        if raw.strip().lower() in {"quit", "q", "exit"}:
            break

        player = normalize(raw)
        if player is None:
            print("Invalid choice. Use rock, paper, scissors (or r/p/s).")
            continue

        # `random` is acceptable here: no security requirement, unlike passwords.
        computer = random.choice(list(BEATS))
        outcome = decide(player, computer)
        score[outcome] += 1

        print(f"Computer chose: {computer}")
        print({"win": "You win!", "lose": "You lose.", "draw": "Draw."}[outcome])

    played = sum(score.values())
    if played:
        print(f"\nRounds: {played} | W:{score['win']} L:{score['lose']} D:{score['draw']}")
    print("Goodbye.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
