import re
from pathlib import Path
import joblib
ROOT = Path(__file__).resolve().parent.parent
_model = joblib.load(ROOT / "models" / "intent.joblib")
def predict_operation(text):
    t = text.lower()
    probs = _model.predict_proba([t])[0]
    classes = list(_model.classes_)
    if not any(ch.isdigit() for ch in t) and "math" in classes:
        probs[classes.index("math")] = -1
    return classes[int(probs.argmax())]
def detect_language(text):
    t = text.lower()
    if "c++" in t or "cpp" in t or "સી++" in t or "सी++" in t:
        return "c++"
    if re.search(r"(?<![a-z])java(?![a-z])", t) or "જાવા" in t or "जावा" in t:
        return "java"
    if re.search(r"(?<![a-z])python(?![a-z])", t) or "પાયથન" in t or "પાઇથન" in t or "पायथन" in t:
        return "python"
    if re.search(r"(?<![a-z+])c(?![a-z+])", t) or "સી ભાષા" in t or "सी भाषा" in t:
        return "c"
    return "python"