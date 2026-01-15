import json
import random
import re
import string
from collections import Counter, defaultdict

def generate_random_text(target_chars=300, seed=7) -> str:
    """
    Generate ~target_chars of simple English-ish text containing spaces and punctuation.
    Deterministic with seed.
    """
    random.seed(seed)

    words = [
        "the","a","this","that","quiet","bright","small","old","new","river","street","window",
        "cat","dog","student","teacher","music","coffee","morning","evening","story","idea",
        "walks","runs","waits","writes","laughs","thinks","finds","keeps","moves","looks",
        "softly","quickly","today","again","almost","never","always","maybe","because","while",
        "and","but","so","yet","if","when","after","before","near","under","over"
    ]
    punct = [".", ".", ".", ",", ",", "!", "?", ";", ":"]

    parts = []
    while len(" ".join(parts)) < target_chars:
        k = random.randint(7, 14)
        sent_words = [random.choice(words) for _ in range(k)]
        sent_words[0] = sent_words[0].capitalize()
        if random.random() < 0.2:
            sent_words[random.randint(1, k - 2)] = "don't"

        sentence = " ".join(sent_words) + random.choice(punct)
        parts.append(sentence)

    text = " ".join(parts)
    return text[:target_chars].rstrip()

def tokenize_words(text: str):
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text.lower())

def ascii_symbol_map(items):
    symbols = [c for c in string.printable if c not in string.whitespace]
    if len(items) > len(symbols):
        raise ValueError("Too many unique words for single-character ASCII mapping.")
    return {item: symbols[i] for i, item in enumerate(sorted(items))}

def build_transition_probs(tokens):
    trans_counts = defaultdict(Counter)
    for w1, w2 in zip(tokens, tokens[1:]):
        trans_counts[w1][w2] += 1

    trans_probs = {}
    for w1, counter in trans_counts.items():
        total = sum(counter.values())
        trans_probs[w1] = {w2: counter[w2] / total for w2 in counter}
    return trans_counts, trans_probs

def convert_to_symbol_matrix(trans_probs, word_to_sym):
    sym_probs = {}
    for w1, nexts in trans_probs.items():
        s1 = word_to_sym[w1]
        sym_probs[s1] = {}
        for w2, p in nexts.items():
            s2 = word_to_sym[w2]
            sym_probs[s1][s2] = p
    return sym_probs

# ---------------------------
# NEW PART: synthesis helpers
# ---------------------------

def weighted_choice(next_dict):
    """
    next_dict: {token: probability}
    returns one token sampled according to probabilities
    """
    r = random.random()
    cum = 0.0
    for token, p in next_dict.items():
        cum += p
        if r <= cum:
            return token
    # fallback in case of rounding
    return next(iter(next_dict))

def synthesize_from_json(json_path="transition_matrix.json", length=50, seed=123, use_symbols=True):
    """
    Load transition matrix from json and synthesize a new word sequence.
    - use_symbols=True uses transition_probs_symbols + symbol_to_word
    - use_symbols=False uses transition_probs_words directly
    """
    random.seed(seed)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if use_symbols:
        trans = data["transition_probs_symbols"]  # symbol -> {symbol: prob}
        sym_to_word = data["symbol_to_word"]      # symbol -> word

        # start from a random symbol that has outgoing transitions
        current = random.choice(list(trans.keys()))
        symbols = [current]

        for _ in range(length - 1):
            nexts = trans.get(current, {})
            if not nexts:
                current = random.choice(list(trans.keys()))
                symbols.append(current)
                continue
            current = weighted_choice(nexts)
            symbols.append(current)

        # decode symbols to words
        words = [sym_to_word[s] for s in symbols]
        return " ".join(words)

    else:
        trans = data["transition_probs_words"]  # word -> {word: prob}
        current = random.choice(list(trans.keys()))
        words = [current]

        for _ in range(length - 1):
            nexts = trans.get(current, {})
            if not nexts:
                current = random.choice(list(trans.keys()))
                words.append(current)
                continue
            current = weighted_choice(nexts)
            words.append(current)

        return " ".join(words)

def main():
    # Build the model and save JSON (your original part)
    text = generate_random_text(target_chars=300, seed=7)
    tokens = tokenize_words(text)

    _, trans_probs = build_transition_probs(tokens)

    vocab = set(tokens)
    word_to_sym = ascii_symbol_map(vocab)
    sym_to_word = {v: k for k, v in word_to_sym.items()}

    sym_probs = convert_to_symbol_matrix(trans_probs, word_to_sym)

    output = {
        "text": text,
        "token_count": len(tokens),
        "unique_words": len(vocab),
        "word_to_symbol": word_to_sym,
        "symbol_to_word": sym_to_word,
        "transition_probs_symbols": sym_probs,
        "transition_probs_words": trans_probs
    }

    with open("transition_matrix.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("Generated text (~300 chars):\n")
    print(text)
    print("\nSaved transition matrix to: transition_matrix.json")
    print(f"Tokens: {len(tokens)}, Unique words: {len(vocab)}")
    print("\nExample mapping (first 10):")
    for (w, s) in sorted(word_to_sym.items())[:10]:
        print(f"  {w:>10s} -> {s}")

    # ---------------------------
    # NEW PART: synthesize text
    # ---------------------------
    print("\n=== Synthesized text (using SYMBOL transitions) ===")
    print(synthesize_from_json("transition_matrix.json", length=60, seed=99, use_symbols=True))

    print("\n=== Synthesized text (using WORD transitions) ===")
    print(synthesize_from_json("transition_matrix.json", length=60, seed=99, use_symbols=False))

if __name__ == "__main__":
    main()
