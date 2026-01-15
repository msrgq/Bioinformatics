import json, random, re
from collections import Counter, defaultdict

def generate_text(target_chars=300, seed=1):
    random.seed(seed)
    words = ["the","cat","walks","near","the","river","and","the","dog","runs",
             "quiet","music","fills","the","street","but","coffee","helps","today"]
    punct = [".", ",", "!", "?", ";", ":"]
    out = []
    while len(" ".join(out)) < target_chars:
        k = random.randint(8, 14)
        sent = [random.choice(words) for _ in range(k)]
        sent[0] = sent[0].capitalize()
        out.append(" ".join(sent) + random.choice(punct))
    return " ".join(out)[:target_chars].rstrip()

def tokenize(text):
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text.lower())

def build_sparse_probs(tokens):
    counts = defaultdict(Counter)
    for a, b in zip(tokens, tokens[1:]):
        counts[a][b] += 1

    probs = {}
    for a, ctr in counts.items():
        total = sum(ctr.values())
        probs[a] = {b: c/total for b, c in ctr.items()}
    return probs

def weighted_choice(next_dict):
    r = random.random()
    cum = 0.0
    for token, p in next_dict.items():
        cum += p
        if r <= cum:
            return token
    return next(iter(next_dict))  # fallback

def synthesize_from_index_json(json_path="transitions_index.json", length=50, seed=42, start_index=None):
    random.seed(seed)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    vocab = data["vocab"]
    trans = data["transition_probs_sparse"] 

    if start_index is None:
        start_index = random.choice(list(trans.keys()))
    else:
        start_index = str(start_index)

    if start_index not in trans:
        raise ValueError("Start index has no outgoing transitions in this model.")

    seq_idx = [start_index]
    current = start_index

    for _ in range(length - 1):
        nexts = trans.get(current, {})
        if not nexts:
            current = random.choice(list(trans.keys()))
            seq_idx.append(current)
            continue

        current = weighted_choice(nexts) 
        seq_idx.append(current)
    words = [vocab[int(i)] for i in seq_idx]
    return " ".join(words)

def main():
    text = generate_text()
    tokens = tokenize(text)
    vocab = sorted(set(tokens))
    w2i = {w:i for i,w in enumerate(vocab)}

    probs_words = build_sparse_probs(tokens)

    probs_idx = {}
    for w1, nexts in probs_words.items():
        i = w2i[w1]
        probs_idx[str(i)] = {str(w2i[w2]): p for w2, p in nexts.items()}

    data = {
        "text": text,
        "vocab": vocab,
        "transition_probs_sparse": probs_idx,
        "notes": "Use vocab[index] to decode indices."
    }

    with open("transitions_index.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(text)
    print("\nSaved: transitions_index.json")
    print("Unique words:", len(vocab))

    print("\n=== Synthesized text (from transitions_index.json) ===")
    print(synthesize_from_index_json("transitions_index.json", length=60, seed=7))

if __name__ == "__main__":
    main()
