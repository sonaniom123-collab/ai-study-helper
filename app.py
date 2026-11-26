from flask import Flask, request
from markupsafe import escape

from core.code_templates import get_code
from core.intent import detect_language, predict_operation
from core.math_solver import solve
from core.programs import find_program, get_program
import re

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

CODE_WORDS = ("program", "code", "java", "python", "c++", "write", "function", "pattern")

PAGE = """
<h2>AI Study Helper</h2>
<p>Ask for a program or a math problem, in one box.</p>
<form action="/go" method="get">
  <input name="q" size="60" placeholder="e.g. multiply two numbers in java   or   factorial in c   or   1/2 + 1/3">
  <button type="submit">Ask</button>
</form>
<h3>Or upload a photo of a math problem</h3>
<form action="/photo" method="post" enctype="multipart/form-data">
  <input type="file" name="photo" accept="image/*">
  <button type="submit">Solve photo</button>
</form>
"""


def looks_like_math(q):
    t = q.lower()
    has_digit = any("0" <= ch <= "9" for ch in t)
    return has_digit and not any(w in t for w in CODE_WORDS)


def math_page(steps):
    body = "<br>".join(str(escape(s)) for s in steps)
    return f"<p>Detected: <b>math problem</b></p><p>{body}</p><a href='/'>Back</a>"


@app.route("/")
def home():
    return PAGE


@app.route("/go")
def go():
    q = request.args.get("q", "").strip()[:200]
    if not q:
        return "Please type something. <a href='/'>Back</a>"

    if looks_like_math(q):
        steps = solve(q)
        if steps:
            return math_page(steps)

    program = find_program(q)
    if program:
        language = detect_language(q)
        result = get_program(program, language)
        return (
            f"<p>Detected: <b>{escape(program)}</b> program in <b>{escape(language)}</b></p>"
            f"<pre>{escape(result)}</pre><a href='/'>Back</a>"
        )

    label = predict_operation(q)

    if label == "math":
        steps = solve(q)
        if not steps:
            return "I understood this as a math problem, but I can't solve this type yet. <a href='/'>Back</a>"
        return math_page(steps)

    language = detect_language(q)
    result = get_code(label, language)
    return (
        f"<p>Detected: <b>{escape(label)}</b> code in <b>{escape(language)}</b></p>"
        f"<pre>{escape(result)}</pre><a href='/'>Back</a>"
    )


MATH_CHARS = re.compile(r"[0-9xX+\-*/×÷().=?%\s]+")


def read_and_solve(file):
    """Try several readings of the photo. Prefer a clean math line over a guess."""
    from core.ocr import candidate_texts

    first_text = ""
    fallback = None
    for text in candidate_texts(file):
        first_text = first_text or text
        lines = [l.strip() for l in text.splitlines() if l.strip()][:10]
        solved = [(l, solve(l)) for l in lines]
        solved = [(l, st) for l, st in solved if st]
        if not solved:
            continue
        clean = len(solved) == len(lines) and all(MATH_CHARS.fullmatch(l) for l, _ in solved)
        if clean:
            return text, solved
        if fallback is None:
            fallback = (text, solved)
    if fallback:
        return fallback
    return first_text, []


@app.route("/photo", methods=["POST"])
def photo():
    f = request.files.get("photo")
    if not f or not f.filename:
        return "Please choose a photo first. <a href='/'>Back</a>"
    try:
        text, solved = read_and_solve(f.stream)
    except Exception as e:
        return f"Could not read the photo: {escape(e)}<br><a href='/'>Back</a>"

    if not text:
        return "No text found in the photo. Try a clearer, closer picture. <a href='/'>Back</a>"

    out = [f"<p><b>Text read from the photo:</b></p><pre>{escape(text)}</pre>"]
    for line, steps in solved:
        body = "<br>".join(str(escape(x)) for x in steps)
        out.append(f"<p><b>Problem:</b> {escape(line)}</p><p>{body}</p><hr>")
    if not solved:
        out.append("<p>I could read the text, but I could not solve it yet.</p>")
    out.append("<p>If the text above is wrong, try a clearer or larger photo.</p><a href='/'>Back</a>")
    return "".join(out)


if __name__ == "__main__":
    app.run(debug=True)