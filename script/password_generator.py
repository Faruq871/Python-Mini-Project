"""Cryptographically secure password generator.
Uses `secrets` (CSPRNG), never `random` (Mersenne Twister, predictable from
observed output). Guarantees at least one character from every enabled class.
"""
from __future__ import annotations

import math
import secrets
import string


def build_pools(
    use_upper: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> list[str]:
    """Return the enabled character classes. Lowercase is always included."""
    pools = [string.ascii_lowercase]
    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_digits:
        pools.append(string.digits)
    if use_symbols:
        pools.append(string.punctuation)
    return pools


def generate_password(
    length: int = 16,
    use_upper: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    """Generate a password of exactly `length` characters."""
    pools = build_pools(use_upper, use_digits, use_symbols)
    if length < len(pools):
        raise ValueError(f"length must be >= {len(pools)} for the selected classes")

    alphabet = "".join(pools)
    # One guaranteed character per class, then fill the remainder uniformly.
    chars = [secrets.choice(pool) for pool in pools]
    chars.extend(secrets.choice(alphabet) for _ in range(length - len(chars)))
    # Secure Fisher-Yates shuffle so the guaranteed characters are not front-loaded.
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def entropy_upper_bound(length: int, alphabet_size: int) -> float:
    """Upper bound in bits: length * log2(alphabet_size).

    An upper bound, not the exact entropy: the 'one per class' constraint makes
    the distribution slightly non-uniform.
    """
    return length * math.log2(alphabet_size)


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    suffix = "[Y/n]" if default else "[y/N]"
    answer = input(f"{prompt} {suffix}: ").strip().lower()
    if not answer:
        return default
    return answer.startswith("y")


def main() -> None:
    print("--- Password Generator ---")
    raw_length = input("Length [16]: ").strip()
    try:
        length = int(raw_length) if raw_length else 16
    except ValueError:
        print("Error: length must be an integer.")
        return

    use_upper = ask_yes_no("Include uppercase letters?")
    use_digits = ask_yes_no("Include digits?")
    use_symbols = ask_yes_no("Include symbols?")

    try:
        password = generate_password(length, use_upper, use_digits, use_symbols)
    except ValueError as exc:
        print(f"Error: {exc}")
        return

    alphabet_size = sum(len(p) for p in build_pools(use_upper, use_digits, use_symbols))
    print(f"\nPassword: {password}")
    print(f"Alphabet size: {alphabet_size}")
    print(f"Entropy upper bound: {entropy_upper_bound(length, alphabet_size):.1f} bits")
    if length < 12:
        print("Warning: lengths below 12 are weak for most threat models.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
