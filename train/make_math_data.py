import csv
import random
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
random.seed(1)
rows = []
def n():
    return random.randint(2, 99)
for _ in range(60):
    a, b, c = n(), n(), n()
    op1, op2 = random.choice("+-*"), random.choice("+-*")
    rows.append((f"{a}{op1}{b}{op2}{c}", "math"))
    rows.append((f"what is {a} {op1} {b}", "math"))
    rows.append((f"calculate ({a}+{b})*{random.randint(2, 9)}", "math"))
for _ in range(40):
    p = random.choice([5, 10, 12, 15, 20, 25, 30, 40, 50])
    rows.append((f"{p} percent of {random.randint(20, 500)}", "math"))
    rows.append((f"what is {p}% of {random.randint(20, 500)}", "math"))
for _ in range(40):
    a, b, c = random.randint(2, 9), random.randint(1, 20), random.randint(20, 60)
    rows.append((f"solve {a}x + {b} = {c}", "math"))
    rows.append((f"{a}x+{b}={c}", "math"))
    rows.append((f"find x if {a}x - {b} = {c}", "math"))
with open(ROOT / "data" / "generated_math.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["text", "label"])
    w.writerows(rows)
print("Wrote", len(rows), "rows")