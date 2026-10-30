"""Length, mass, and temperature converter.

Linear units are stored as exact factors relative to a base unit, so any
pair converts in both directions without hardcoding reciprocals.
Imperial factors below are exact by international definition, not rounded.
"""
from __future__ import annotations

from typing import Callable

LENGTH_TO_METERS: dict[str, float] = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
    "in": 0.0254,        # exact
    "ft": 0.3048,        # exact
    "mi": 1609.344,      # exact
}

MASS_TO_KILOGRAMS: dict[str, float] = {
    "g": 0.001,
    "kg": 1.0,
    "oz": 0.028349523125,  # exact
    "lb": 0.45359237,      # exact
}

LINEAR_TABLES = (LENGTH_TO_METERS, MASS_TO_KILOGRAMS)

TO_CELSIUS: dict[str, Callable[[float], float]] = {
    "c": lambda v: v,
    "f": lambda v: (v - 32.0) * 5.0 / 9.0,
    "k": lambda v: v - 273.15,
}

FROM_CELSIUS: dict[str, Callable[[float], float]] = {
    "c": lambda v: v,
    "f": lambda v: v * 9.0 / 5.0 + 32.0,
    "k": lambda v: v + 273.15,
}


def convert(value: float, source: str, target: str) -> float:
    """Convert `value` from `source` unit to `target` unit."""
    source, target = source.strip().lower(), target.strip().lower()

    if source in TO_CELSIUS and target in TO_CELSIUS:
        celsius = TO_CELSIUS[source](value)
        if celsius < -273.15:
            raise ValueError("temperature below absolute zero")
        return FROM_CELSIUS[target](celsius)

    for table in LINEAR_TABLES:
        if source in table and target in table:
            return value * table[source] / table[target]

    raise ValueError(f"cannot convert {source!r} to {target!r} (unknown or incompatible units)")


def main() -> None:
    print("--- Unit Converter ---")
    print("Length: " + ", ".join(LENGTH_TO_METERS))
    print("Mass:   " + ", ".join(MASS_TO_KILOGRAMS))
    print("Temp:   c, f, k")

    source = input("Convert from: ")
    target = input("Convert to:   ")
    try:
        value = float(input("Value: ").strip())
        result = convert(value, source, target)
    except ValueError as exc:
        print(f"Error: {exc}")
        return

    print(f"{value:g} {source.lower()} = {result:.6g} {target.lower()}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
