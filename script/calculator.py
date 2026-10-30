"""Command-line calculator supporting +, -, *, /.

Logic is separated from I/O so `calculate()` can be unit-tested directly.
"""
from __future__ import annotations

import operator
from typing import Callable

# Dispatch table: O(1) average lookup, avoids a long if/elif chain.
OPERATIONS: dict[str, Callable[[float, float], float]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


def calculate(a: float, op: str, b: float) -> float:
    """Apply `op` to `a` and `b`.

    Raises:
        ValueError: unsupported operator.
        ZeroDivisionError: division by zero.
    """
    if op not in OPERATIONS:
        raise ValueError(f"unsupported operator {op!r} (use +, -, *, /)")
    return OPERATIONS[op](a, b)


def main() -> None:
    print("--- Simple Calculator ---")
    raw_a = input("First number: ").strip()
    op = input("Operator (+, -, *, /): ").strip()
    raw_b = input("Second number: ").strip()

    try:
        a, b = float(raw_a), float(raw_b)
        result = calculate(a, op, b)
    except ValueError as exc:
        print(f"Error: {exc}")
        return
    except ZeroDivisionError:
        print("Error: division by zero is undefined.")
        return

    print(f"Result: {a} {op} {b} = {result}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
