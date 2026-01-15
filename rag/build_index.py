import os, json
from sklearn.feature_extraction.text import TfidfVectorizer

DOC_DIR = "data/internal_docs"
OUT_PATH = "rag/index.json"

def load_docs():
    docs = []
    for fn in os.listdir(DOC_DIR):
        if fn.endswith(".md"):
            path = os.path.join(DOC_DIR, fn)
            with open(path, "r", encoding="utf-8") as f:
                docs.append({"id": fn, "text": f.read()})
    return docs

docs = load_docs()
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform([d["text"] for d in docs])

payload = {
    "docs": docs,
    "vocab": vectorizer.vocabulary_,
    "idf": vectorizer.idf_.tolist(),
}
with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(payload, f)

print(f"Saved {len(docs)} docs to {OUT_PATH}")
