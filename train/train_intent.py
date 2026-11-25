from pathlib import Path
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
ROOT = Path(__file__).resolve().parent.parent
frames = [pd.read_csv(p, encoding="utf-8") for p in sorted((ROOT / "data").glob("*.csv"))]
df = pd.concat(frames, ignore_index=True)
print(df["label"].value_counts())
def build_model():
    return make_pipeline(
        TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4)),
        LogisticRegression(max_iter=1000, class_weight="balanced"),
    )
X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
)
check = build_model()
check.fit(X_train, y_train)
print("Test accuracy:", round(check.score(X_test, y_test), 2))
final = build_model()
final.fit(df["text"], df["label"])
(ROOT / "models").mkdir(exist_ok=True)
joblib.dump(final, ROOT / "models" / "intent.joblib")
print("Saved models/intent.joblib")