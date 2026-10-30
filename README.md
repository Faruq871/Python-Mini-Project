
# Python Mini Projects Collection

Six small command-line programs written in Python, plus a Quarto document that
analyses the logic, data structures, and time/space complexity of each one.

The scripts are deliberately simple. The purpose of the repository is to pair
working code with an explicit, honest written analysis — including the cases
where Big-O notation says very little of practical value.

**Documentation:** https://github.com/Faruq871/Python-Mini-Project

## Contents

| # | Script | What it does | Main concepts |
|---|--------|--------------|---------------|
| 1 | `calculator.py` | Four-function arithmetic | Dispatch table, exception handling |
| 2 | `cash_register.py` | Menu, cart, receipt, change | Dictionaries, integer-cent money, input validation |
| 3 | `guess_number.py` | Higher/lower guessing game | Loops, RNG, search strategy vs. program complexity |
| 4 | `password_generator.py` | Secure random passwords | CSPRNG, entropy, character-class coverage |
| 5 | `unit_converter.py` | Length, mass, temperature | Base-unit factor tables, affine vs. linear conversion |
| 6 | `rock_paper_scissors.py` | Game vs. random opponent | Rule encoding as a cyclic map, state accumulation |

## Requirements

- Python **3.9+**
- **No third-party dependencies.** Standard library only.
- [Quarto CLI](https://quarto.org/docs/get-started/) — only if you want to render the documentation locally.

## Quick start

```bash
git clone https://github.com/<your-username>/python-mini-projects-collection.git
cd python-mini-projects-collection

python scripts/calculator.py
python scripts/cash_register.py
python scripts/guess_number.py
python scripts/password_generator.py
python scripts/unit_converter.py
python scripts/rock_paper_scissors.py
```

All scripts are interactive and read from stdin. Press `Ctrl+C` to exit at any prompt.

### Example session

```text
$ python scripts/cash_register.py
--- Cash Register ---

Menu:
  coffee        $2.50
  tea           $2.00
  sandwich      $5.50
  donut         $1.75

Item name (or 'done' to check out): coffee
Quantity of coffee: 2

Item name (or 'done' to check out): done

--- Receipt ---
coffee     x2      $5.00
TOTAL              $5.00
Payment amount: 20
Paid:   $20.00
Change: $15.00

```
### Using the logic without the CLI

Each script separates its core logic from I/O, so the functions are importable and testable:

```python
from scripts.calculator import calculate
from scripts.unit_converter import convert
from scripts.password_generator import generate_password
from scripts.rock_paper_scissors import decide

calculate(10, "/", 4)              # 2.5
convert(100, "cm", "in")           # 39.37007874015748
convert(0, "c", "f")               # 32.0
len(generate_password(20))         # 20
decide("rock", "scissors")         # 'win'
```

Run from the repository root. There is no package installation step; if you prefer `import scripts.x` to work from anywhere, add an empty `scripts/__init__.py` and a `pyproject.toml`.

## Complexity summary

Average-case, excluding interactive I/O. See the Quarto document for the assumptions behind each claim.

| Project | Time | Space |
|---|---|---|
| Calculator | O(1) | O(1) |
| Cash Register | O(U), unique line items | O(U) |
| Guess the Number | O(K), valid guesses | O(1) |
| Password Generator | O(L), password length | O(L) |
| Unit Converter | O(1) | O(1) |
| Rock–Paper–Scissors | O(1) per round | O(1) |

Two claims worth reading carefully:
- **Guess the Number has no finite worst-case bound.** The loop has no attempt cap. O(log n) describes a *player using binary search*, not the program.
- **Most of these bounds are uninformative.** With inputs this small, constant factors and terminal I/O dominate. The table is a learning exercise, not a performance result. No benchmarks were run.

## Design notes

- **`secrets` vs. `random`:** The password generator uses `secrets` (OS CSPRNG) for both character selection and shuffling. `random` uses Mersenne Twister, whose state is recoverable from observed output — it is unsuitable for credentials. Rock–Paper–Scissors and the guessing game use `random`, which is correct there: no adversary, no security requirement.
- **Money as integer cents:** The cash register never stores money as a float. Binary floating point cannot represent most decimal fractions exactly, and summing float prices accumulates error. `Decimal` is used only to parse input and format output.
- **Exact conversion factors:** Imperial factors are exact by definition (1 in = 0.0254 m, 1 lb = 0.45359237 kg), not rounded approximations. Storing one factor per unit relative to a base unit means inverse conversions are automatic and round-trips stay consistent.
- **Password entropy is an upper bound:** Guaranteeing one character per class makes the output distribution slightly non-uniform, so `L × log₂|A|` overstates true entropy marginally. The document states this rather than reporting it as exact.

## Known limitations

- No persistence: carts, scores, and game state are lost on exit.
- No automated test suite yet. The pure functions are structured to make one straightforward to add.
- The calculator accepts `nan` and `inf` as inputs, since `float()` does; it does not reject them.
- The password generator uses `string.punctuation`, which includes quotes and backslashes that some systems reject in passwords.
- Single-user, single-currency, no tax or discount logic in the cash register.
- No CLI argument parsing; everything is interactive prompts.

## Repository layout

```text
.
├── scripts/                  
├── index.qmd                 
├── _quarto.yml              
├── .github/workflows/        
└── README.md
```

## Possible extensions

- `pytest` suite covering the pure functions, including edge cases (division by zero, empty cart, absolute zero, minimum password length).
- `argparse` support for non-interactive use and shell scripting.
- Additional unit categories (volume, area, data size) — the factor-table design makes these one-dict additions.
- Best-of-N mode and non-uniform opponent strategies for Rock–Paper–Scissors.
