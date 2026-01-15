import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

INDEX_PATH = "rag/index.json"
TOP_K = 2

def cosine_sim(a, b):
    denom = (np.linalg.norm(a) * np.linalg.norm(b)) + 1e-9
    return float(np.dot(a, b) / denom)

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    payload = json.load(f)

docs = payload["docs"]
vocab = payload["vocab"]
idf = np.array(payload["idf"])

vectorizer = TfidfVectorizer(stop_words="english", vocabulary=vocab)
vectorizer._tfidf.idf_ = idf

doc_matrix = vectorizer.fit_transform([d["text"] for d in docs]).toarray()

q = input("Question: ").strip()
q_vec = vectorizer.transform([q]).toarray()[0]

scores = [(docs[i]["id"], cosine_sim(q_vec, doc_matrix[i])) for i in range(len(docs))]
scores.sort(key=lambda x: x[1], reverse=True)

top = scores[:TOP_K]
print("\nTop docs:")
for doc_id, s in top:
    print(f"- {doc_id} (score={s:.3f})")

print("\n---\nContext to paste into your LLM:\n")
for doc_id, _ in top:
    text = next(d["text"] for d in docs if d["id"] == doc_id)
    print(f"[{doc_id}]\n{text}\n")
