import csv
import itertools
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
ops = {
    "addition": ["add two numbers", "sum of two numbers", "addition of two numbers",
                 "plus two numbers", "find the total of two numbers", "add a and b"],
    "subtraction": ["subtract two numbers", "subtraction of two numbers", "difference of two numbers",
                    "minus two numbers", "subtract b from a", "find the difference of a and b"],
    "multiplication": ["multiply two numbers", "multiplication of two numbers", "product of two numbers",
                       "times two numbers", "multiply a and b", "find the product of a and b"],
    "division": ["divide two numbers", "division of two numbers", "quotient of two numbers",
                 "divide a by b", "find the quotient of a and b", "division of a and b"],
}
starts = ["", "write a program to ", "give me code to ", "program for ", "how to "]
langs = ["", " in python", " in java", " in c", " in c++"]
rows = []
for label, phrases in ops.items():
    for s, p, l in itertools.product(starts, phrases, langs):
        rows.append((f"{s}{p}{l}", label))
with open(ROOT / "data" / "generated_data.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["text", "label"])
    w.writerows(rows)
print("Wrote", len(rows), "rows")