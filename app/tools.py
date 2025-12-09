from pathlib import Path


def load_notes():
    """
    Load all .txt files from the data/ folder.
    Returns a list of dicts: [{"path": Path, "content": str}, ...]
    """
    data_path = Path("data")
    if not data_path.exists():
        raise FileNotFoundError("data/ folder not found. Create it and add .txt files.")

    docs = []
    for file in data_path.glob("*.txt"):
        text = file.read_text(encoding="utf-8", errors="ignore")
        docs.append({"path": file, "content": text})

    if not docs:
        raise ValueError("No .txt files found in data/. Add at least one notes file.")

    return docs


def search_notes(notes, query: str) -> str:
    """
    Naive keyword search over loaded notes.

    - Splits query into words
    - Scores each document by keyword frequency
    - Returns top snippets as a single string
    """
    query_words = [w.lower() for w in query.split() if w.strip()]
    if not query_words:
        return ""

    scored = []
    for doc in notes:
        text_lower = doc["content"].lower()
        score = sum(text_lower.count(w) for w in query_words)
        if score > 0:
            scored.append((score, doc))

    if not scored:
        return ""

    scored.sort(key=lambda x: x[0], reverse=True)

    snippets = []
    for score, doc in scored[:3]:
        content = doc["content"]
        snippet = content[:800]
        snippets.append(f"From file: {doc['path'].name}\n\n{snippet}")

    return "\n\n-----------------------------\n\n".join(snippets)


def calculate(expr: str) -> str:
    """
    Simple arithmetic calculator.
    Evaluates a Python expression: '2+3*4', '25*(3+7)', etc.
    """
    try:
        result = eval(expr, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"
