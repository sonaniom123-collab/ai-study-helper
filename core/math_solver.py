import ast
import re
from math import gcd

from sympy import Poly, Rational, Symbol
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

x = Symbol("x")
TRANSFORMS = standard_transformations + (implicit_multiplication_application,)

OPS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
}
SYMBOL = {ast.Add: "+", ast.Sub: "-", ast.Mult: "×", ast.Div: "÷"}


def fmt(n):
    n = float(n)
    if n == int(n):
        return str(int(n))
    return f"{n:.4f}".rstrip("0").rstrip(".")


def show(v):
    v = Rational(v)
    if v.is_Integer:
        return str(v)
    return f"{v} (= {fmt(v)})"


class _FoldSign(ast.NodeTransformer):
    def visit_UnaryOp(self, node):
        self.generic_visit(node)
        if isinstance(node.op, (ast.USub, ast.UAdd)) and isinstance(node.operand, ast.Constant):
            v = node.operand.value
            return ast.Constant(-v if isinstance(node.op, ast.USub) else v)
        return node


def _reduce_once(node):
    if isinstance(node, ast.BinOp):
        if type(node.op) not in OPS:
            raise ValueError("unsupported operator")
        left, right = node.left, node.right
        if isinstance(left, ast.Constant) and isinstance(right, ast.Constant):
            if isinstance(node.op, ast.Div) and right.value == 0:
                raise ZeroDivisionError
            value = OPS[type(node.op)](left.value, right.value)
            if isinstance(value, float):
                value = round(value, 10)
                if value == int(value):
                    value = int(value)
            desc = f"{fmt(left.value)} {SYMBOL[type(node.op)]} {fmt(right.value)} = {fmt(value)}"
            return ast.Constant(value), desc
        res = _reduce_once(left)
        if res:
            node.left = res[0]
            return node, res[1]
        res = _reduce_once(right)
        if res:
            node.right = res[0]
            return node, res[1]
    elif isinstance(node, ast.UnaryOp):
        if isinstance(node.operand, ast.Constant):
            v = node.operand.value
            v = -v if isinstance(node.op, ast.USub) else v
            return ast.Constant(v), f"Apply the sign: {fmt(v)}"
        res = _reduce_once(node.operand)
        if res:
            node.operand = res[0]
            return node, res[1]
    return None


def solve_arithmetic(expr):
    try:
        tree = ast.parse(expr, mode="eval")
        node = _FoldSign().visit(tree).body
        steps = [f"Expression: {ast.unparse(node)}", "Rule: brackets first, then × and ÷, then + and -, left to right."]
        i = 0
        while not isinstance(node, ast.Constant):
            res = _reduce_once(node)
            if res is None:
                return None
            node, desc = res
            i += 1
            if isinstance(node, ast.Constant):
                steps.append(f"Step {i}: {desc}")
            else:
                steps.append(f"Step {i}: {desc}, so we get {ast.unparse(node)}")
        steps.append(f"Answer: {fmt(node.value)}")
        return steps
    except ZeroDivisionError:
        return ["You cannot divide by zero."]
    except (SyntaxError, ValueError, TypeError):
        return None


def solve_percentage(p, n):
    p, n = Rational(p), Rational(n)
    return [
        f"{fmt(p)}% of {fmt(n)} means ({fmt(p)} ÷ 100) × {fmt(n)}",
        f"Step 1: multiply {fmt(p)} × {fmt(n)} = {fmt(p * n)}",
        f"Step 2: divide {fmt(p * n)} ÷ 100 = {fmt(p * n / 100)}",
        f"Answer: {fmt(p * n / 100)}",
    ]


def solve_equation(text):
    try:
        left, right = text.split("=", 1)
        lhs = parse_expr(left, local_dict={"x": x}, transformations=TRANSFORMS)
        rhs = parse_expr(right, local_dict={"x": x}, transformations=TRANSFORMS)
        poly = Poly(lhs - rhs, x)
        if poly.degree() != 1:
            return ["Only simple equations like 2x + 3 = 11 are supported for now."]
        a, b = [Rational(str(c)) for c in poly.all_coeffs()]
    except Exception:
        return None
    sol = -b / a
    return [
        f"Equation: {left.strip()} = {right.strip()}",
        f"Step 1: put the x terms on the left and the numbers on the right: {show(a)}x = {show(-b)}",
        f"Step 2: divide both sides by {show(a)}: x = {show(-b)} ÷ {show(a)}",
        f"Answer: x = {show(sol)}",
        f"Check: left side = {show(lhs.subs(x, sol))}, right side = {show(rhs.subs(x, sol))}",
    ]


# ---------- fractions ----------

FRACTION = re.compile(r"(\d+)\s*/\s*(\d+)\s*([+\-*/])\s*(\d+)\s*/\s*(\d+)")


def _lcm(a, b):
    return a * b // gcd(a, b)


def _simplify_step(n, d):
    g = gcd(abs(n), d)
    if g > 1:
        return n // g, d // g, f"Simplify: divide top and bottom by {g}: {n}/{d} = {_frac_text(n // g, d // g)}"
    return n, d, None


def _frac_text(n, d):
    return str(n) if d == 1 else f"{n}/{d}"


def solve_fraction(a, b, op, c, d):
    if b == 0 or d == 0:
        return ["A fraction cannot have 0 as its bottom number."]
    steps = [f"Problem: {a}/{b} {op} {c}/{d}"]
    if op in "+-":
        L = _lcm(b, d)
        m1, m2 = L // b, L // d
        n1, n2 = a * m1, c * m2
        steps.append(f"Step 1: make the bottom numbers equal. LCM of {b} and {d} is {L}.")
        steps.append(f"Step 2: {a}/{b} = {n1}/{L} and {c}/{d} = {n2}/{L}")
        n = n1 + n2 if op == "+" else n1 - n2
        word = "Add" if op == "+" else "Subtract"
        steps.append(f"Step 3: {word} the top numbers: {n1} {op} {n2} = {n}, so we get {n}/{L}")
        den = L
    elif op == "*":
        n, den = a * c, b * d
        steps.append("Rule: multiply top × top and bottom × bottom.")
        steps.append(f"Step 1: {a} × {c} = {n} and {b} × {d} = {den}, so we get {n}/{den}")
    else:
        if c == 0:
            return ["You cannot divide by zero."]
        steps.append(f"Rule: to divide, flip the second fraction and multiply: {a}/{b} × {d}/{c}")
        n, den = a * d, b * c
        steps.append(f"Step 1: {a} × {d} = {n} and {b} × {c} = {den}, so we get {n}/{den}")
    if den < 0:
        n, den = -n, -den
    n2_, d2_, note = _simplify_step(n, den)
    if note:
        count = sum(1 for line in steps if line.startswith("Step"))
        steps.append(f"Step {count + 1}: {note}")
    if d2_ == 1:
        steps.append(f"Answer: {n2_}")
    else:
        steps.append(f"Answer: {n2_}/{d2_} (= {fmt(n2_ / d2_)})")
    return steps


# ---------- area and perimeter ----------

NUM = re.compile(r"\d+(?:\.\d+)?")
PI = 3.14


def _nums(t):
    return [float(v) for v in NUM.findall(t)]


def solve_geometry(t):
    nums = _nums(t)
    want_area = "area" in t
    want_perimeter = "perimeter" in t or "circumference" in t
    if not (want_area or want_perimeter):
        return None

    if "rectangle" in t:
        if len(nums) < 2:
            return ["Please give the length and the width, for example: area of rectangle length 5 width 3"]
        l, w = nums[0], nums[1]
        if want_area:
            return [f"Rectangle: length = {fmt(l)}, width = {fmt(w)}",
                    "Formula: area = length × width",
                    f"Step 1: {fmt(l)} × {fmt(w)} = {fmt(l * w)}",
                    f"Answer: area = {fmt(l * w)} square units"]
        return [f"Rectangle: length = {fmt(l)}, width = {fmt(w)}",
                "Formula: perimeter = 2 × (length + width)",
                f"Step 1: {fmt(l)} + {fmt(w)} = {fmt(l + w)}",
                f"Step 2: 2 × {fmt(l + w)} = {fmt(2 * (l + w))}",
                f"Answer: perimeter = {fmt(2 * (l + w))} units"]

    if "square" in t:
        if len(nums) < 1:
            return ["Please give the side, for example: area of square side 4"]
        s = nums[0]
        if want_area:
            return [f"Square: side = {fmt(s)}",
                    "Formula: area = side × side",
                    f"Step 1: {fmt(s)} × {fmt(s)} = {fmt(s * s)}",
                    f"Answer: area = {fmt(s * s)} square units"]
        return [f"Square: side = {fmt(s)}",
                "Formula: perimeter = 4 × side",
                f"Step 1: 4 × {fmt(s)} = {fmt(4 * s)}",
                f"Answer: perimeter = {fmt(4 * s)} units"]

    if "circle" in t:
        if len(nums) < 1:
            return ["Please give the radius, for example: area of circle radius 7"]
        steps = []
        r = nums[0]
        if "diameter" in t:
            steps.append(f"Diameter = {fmt(r)}, so radius = {fmt(r)} ÷ 2 = {fmt(r / 2)}")
            r = r / 2
        else:
            steps.append(f"Circle: radius = {fmt(r)} (using π = 3.14)")
        if want_area:
            steps += ["Formula: area = π × r × r",
                      f"Step 1: {fmt(r)} × {fmt(r)} = {fmt(r * r)}",
                      f"Step 2: 3.14 × {fmt(r * r)} = {fmt(PI * r * r)}",
                      f"Answer: area = {fmt(PI * r * r)} square units"]
        else:
            steps += ["Formula: circumference = 2 × π × r",
                      f"Step 1: 2 × 3.14 = 6.28",
                      f"Step 2: 6.28 × {fmt(r)} = {fmt(2 * PI * r)}",
                      f"Answer: circumference = {fmt(2 * PI * r)} units"]
        return steps

    if "triangle" in t:
        if want_area:
            if len(nums) < 2:
                return ["Please give the base and the height, for example: area of triangle base 6 height 4"]
            b, h = nums[0], nums[1]
            return [f"Triangle: base = {fmt(b)}, height = {fmt(h)}",
                    "Formula: area = ½ × base × height",
                    f"Step 1: {fmt(b)} × {fmt(h)} = {fmt(b * h)}",
                    f"Step 2: half of {fmt(b * h)} = {fmt(b * h / 2)}",
                    f"Answer: area = {fmt(b * h / 2)} square units"]
        if len(nums) < 3:
            return ["Please give the three sides, for example: perimeter of triangle sides 3 4 5"]
        a_, b_, c_ = nums[:3]
        return [f"Triangle: sides = {fmt(a_)}, {fmt(b_)}, {fmt(c_)}",
                "Formula: perimeter = sum of all three sides",
                f"Step 1: {fmt(a_)} + {fmt(b_)} + {fmt(c_)} = {fmt(a_ + b_ + c_)}",
                f"Answer: perimeter = {fmt(a_ + b_ + c_)} units"]

    return ["I can do area and perimeter of a rectangle, square, circle and triangle."]


# ---------- main entry ----------

PERCENT = re.compile(r"(\d+(?:\.\d+)?)\s*(?:%|percent|per cent)\s*(?:of)?\s*(\d+(?:\.\d+)?)", re.I)

WORD_OPS = [
    (r"\bmultiplied\s+by\b", " * "),
    (r"\bdivided\s+by\b", " / "),
    (r"\bplus\b", " + "),
    (r"\bminus\b", " - "),
    (r"\btimes\b", " * "),
]


def words_to_symbols(t):
    for pattern, symbol in WORD_OPS:
        t = re.sub(pattern, symbol, t)
    return t


LEADING_NUMBER = re.compile(r"^\s*(?:q(?:uestion)?\.?\s*)?\d+\s*[.)]\s+", re.I)


def clean_problem(text):
    text = LEADING_NUMBER.sub("", text.strip())
    text = re.sub(r"\s*=\s*[?%]*\s*$", "", text)
    text = re.sub(r"[=?\s]+$", "", text)
    return text


def solve(text):
    text = clean_problem(text)
    t = text.lower().replace("×", "*").replace("÷", "/")
    t = words_to_symbols(t)

    if "=" in t:
        m = re.search(r"[0-9x+\-*/(). ]+=[0-9x+\-*/(). ]+", t)
        return solve_equation(m.group().strip()) if m else None

    m = PERCENT.search(t)
    if m:
        return solve_percentage(m.group(1), m.group(2))

    geo = solve_geometry(t)
    if geo:
        return geo

    m = FRACTION.search(t)
    if m:
        a, b, op, c, d = int(m.group(1)), int(m.group(2)), m.group(3), int(m.group(4)), int(m.group(5))
        return solve_fraction(a, b, op, c, d)

    t = re.sub(r"(?<=[\d)])\s*x\s*(?=[\d(])", "*", t)
    candidates = [c.strip().rstrip(". ") for c in re.findall(r"[\d(][\d+\-*/().\s]*", t)]
    candidates = [c for c in candidates if re.search(r"[+\-*/]", c)]
    if not candidates:
        return None
    best = max(candidates, key=len)
    leftover = t.replace(best, " ", 1)
    if re.search(r"[\d%=]", leftover):
        return None
    return solve_arithmetic(best)


if __name__ == "__main__":
    tests = [
        "12+35*2", "what is (2+3)*4", "25 percent of 200", "2x + 3 = 11", "7/2",
        "5 plus 3", "10 minus 4", "6 times 7", "20 divided by 4", "what is 5 plus 3 times 2",
        "1/2 + 1/3", "3/4 - 1/4", "2/3 * 3/4", "1/2 / 1/4", "1/2 + 1/2",
        "area of rectangle length 5 width 3", "perimeter of rectangle length 5 width 3",
        "area of square side 4", "perimeter of square side 4",
        "area of circle radius 7", "circumference of circle diameter 10",
        "area of triangle base 6 height 4", "perimeter of triangle sides 3 4 5",
    ]
    for q in tests:
        print("Q:", q)
        print("\n".join(solve(q) or ["Could not understand"]))
        print()