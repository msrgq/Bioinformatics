# ex2.py
# CpG-style Markov classifier for POETRY:
# - Build two word-transition models (Eminescu vs Nichita Stănescu)
# - Compute Log-Likelihood Ratio (LLR) transition matrix
# - Scan a 3rd mixed text with a sliding window and plot which poet it resembles

import math
import re
from collections import Counter, defaultdict
from typing import List, Dict, Tuple

import matplotlib.pyplot as plt


# -----------------------------
# 1) IO + TOKENIZATION
# -----------------------------

def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def tokenize_ro(text: str) -> List[str]:
    """
    Romanian-friendly tokenization:
    - keeps letters including diacritics: ăâîșşțţ
    - keeps apostrophes inside words (rare in RO, but safe)
    - lowercases
    """
    text = text.lower()
    # include both comma variants for s/t with cedilla (ş/ţ) and comma (ș/ț)
    return re.findall(r"[a-zăâîșşțţ]+(?:'[a-zăâîșşțţ]+)?", text, flags=re.IGNORECASE)

def equalize_lengths(a: List[str], b: List[str]) -> Tuple[List[str], List[str]]:
    """Cut both lists to the same (minimum) length so poems are comparable."""
    m = min(len(a), len(b))
    return a[:m], b[:m]


# -----------------------------
# 2) VOCAB + MAPPING (word -> id)
# -----------------------------

def build_vocab(*token_lists: List[str]) -> List[str]:
    vocab = sorted(set().union(*[set(toks) for toks in token_lists]))
    return vocab

def make_w2i(vocab: List[str]) -> Dict[str, int]:
    return {w: i for i, w in enumerate(vocab)}

def tokens_to_ids(tokens: List[str], w2i: Dict[str, int]) -> List[int]:
    return [w2i[w] for w in tokens if w in w2i]


# -----------------------------
# 3) TRANSITION COUNTS / PROBS (sparse)
# -----------------------------

def transition_counts_sparse(ids: List[int]) -> Dict[int, Counter]:
    """
    Sparse transition counts: counts[from_id][to_id] += 1
    """
    counts = defaultdict(Counter)
    for a, b in zip(ids, ids[1:]):
        counts[a][b] += 1
    return counts

def transition_probs_sparse(counts: Dict[int, Counter], vocab_size: int, alpha: float = 1.0) -> Dict[int, Dict[int, float]]:
    """
    Laplace smoothing (add-alpha) in a *conceptual* full matrix:
      P(to|from) = (c + alpha) / (row_sum + alpha * V)

    We store only the probabilities for observed transitions + (implicitly) smoothed mass
    for unseen transitions is still non-zero, but we’ll handle unseen transitions during scoring.
    """
    probs = {}
    for frm, ctr in counts.items():
        row_sum = sum(ctr.values())
        denom = row_sum + alpha * vocab_size
        probs[frm] = {to: (c + alpha) / denom for to, c in ctr.items()}
        # Note: unseen transitions from frm have probability alpha/denom
        probs[frm]["__DENOM__"] = denom
        probs[frm]["__ALPHA__"] = alpha
        probs[frm]["__ROWSUM__"] = row_sum
    return probs

def get_prob(probs: Dict[int, Dict[int, float]], frm: int, to: int, vocab_size: int, alpha: float) -> float:
    """
    Return smoothed probability P(to|frm), even if (frm->to) not observed.
    If frm never appears as a 'from' in training, use uniform distribution 1/V.
    """
    if frm not in probs:
        return 1.0 / vocab_size

    row = probs[frm]
    if to in row:
        return row[to]

    denom = row["__DENOM__"]
    # unseen transition:
    return alpha / denom


# -----------------------------
# 4) LOG-LIKELIHOOD RATIO MATRIX (implicit) + SCORING
# -----------------------------

def score_ids_llr(window_ids: List[int],
                  probs_E: Dict[int, Dict[int, float]],
                  probs_S: Dict[int, Dict[int, float]],
                  vocab_size: int,
                  alpha: float) -> float:
    """
    Compute LLR(window) = sum_{transitions} log2( P_E(to|from) / P_S(to|from) )
    Positive => more Eminescu-like, negative => more Stănescu-like.
    """
    llr = 0.0
    for a, b in zip(window_ids, window_ids[1:]):
        pE = get_prob(probs_E, a, b, vocab_size, alpha)
        pS = get_prob(probs_S, a, b, vocab_size, alpha)
        llr += math.log(pE / pS, 2)
    return llr


# -----------------------------
# 5) SLIDING WINDOW SCAN + PLOT
# -----------------------------

def sliding_window_scan(test_ids: List[int],
                        probs_E: Dict[int, Dict[int, float]],
                        probs_S: Dict[int, Dict[int, float]],
                        vocab_size: int,
                        alpha: float,
                        window_size: int = 60,
                        step: int = 5) -> Tuple[List[int], List[float]]:
    """
    Scan test_ids with a sliding window:
    - window_size in WORDS
    - step in WORDS
    Returns:
      positions: starting index of each window in the test token stream
      scores: LLR scores for each window
    """
    positions = []
    scores = []

    if len(test_ids) < window_size:
        raise ValueError(f"Test text too short ({len(test_ids)} tokens). Need at least window_size={window_size}.")

    for start in range(0, len(test_ids) - window_size + 1, step):
        window = test_ids[start:start + window_size]
        s = score_ids_llr(window, probs_E, probs_S, vocab_size, alpha)
        positions.append(start)
        scores.append(s)

    return positions, scores

def plot_scan(positions: List[int], scores: List[float], title: str):
    """
    Plot LLR scores and shade background:
    - green-ish above 0 (Eminescu-like)
    - orange-ish below 0 (Stănescu-like)
    """
    plt.figure(figsize=(12, 5))
    plt.plot(positions, scores, linewidth=1.8)
    plt.axhline(0.0, linewidth=1.0)

    # background shading by sign
    for i in range(len(scores) - 1):
        x0, x1 = positions[i], positions[i + 1]
        if scores[i] >= 0:
            plt.axvspan(x0, x1, alpha=0.12)
        else:
            plt.axvspan(x0, x1, alpha=0.12)

    plt.title(title)
    plt.xlabel("Word index (window start)")
    plt.ylabel("LLR score (log2 Eminescu / Stănescu)")
    plt.grid(True, alpha=0.25)
    plt.show()


# -----------------------------
# 6) MAIN
# -----------------------------

def main():
    # -----------------------------
    # FILES (edit these paths)
    # -----------------------------
    EM_PATH = "eminescu.txt"
    ST_PATH = "stanescu.txt"
    TEST_PATH = "test_poems.txt"  # your uploaded test poems file

    # -----------------------------
    # PARAMETERS
    # -----------------------------
    alpha = 1.0          # Laplace smoothing
    window_size = 60     # words per window
    step = 5             # slide by 5 words

    # -----------------------------
    # LOAD + TOKENIZE
    # -----------------------------
    em_text = load_text(EM_PATH)
    st_text = load_text(ST_PATH)
    test_text = load_text(TEST_PATH)

    em_tokens = tokenize_ro(em_text)
    st_tokens = tokenize_ro(st_text)
    test_tokens = tokenize_ro(test_text)

    if len(em_tokens) < 30 or len(st_tokens) < 30:
        raise ValueError("Training poems are too short. Use longer poems or larger excerpts.")

    # Make training poems comparable length
    em_tokens, st_tokens = equalize_lengths(em_tokens, st_tokens)

    # Build shared vocab across all texts (important for consistent ids)
    vocab = build_vocab(em_tokens, st_tokens, test_tokens)
    w2i = make_w2i(vocab)
    V = len(vocab)

    # Convert to ids
    em_ids = tokens_to_ids(em_tokens, w2i)
    st_ids = tokens_to_ids(st_tokens, w2i)
    test_ids = tokens_to_ids(test_tokens, w2i)

    print("=== DATA SUMMARY ===")
    print(f"Eminescu tokens (used): {len(em_ids)}")
    print(f"Stanescu tokens (used): {len(st_ids)}")
    print(f"Test tokens:            {len(test_ids)}")
    print(f"Vocabulary size:        {V}")
    print(f"Window size / step:     {window_size} / {step}")
    print(f"Smoothing alpha:        {alpha}")

    # -----------------------------
    # BUILD TRANSITION MODELS
    # -----------------------------
    counts_E = transition_counts_sparse(em_ids)
    counts_S = transition_counts_sparse(st_ids)

    probs_E = transition_probs_sparse(counts_E, V, alpha=alpha)
    probs_S = transition_probs_sparse(counts_S, V, alpha=alpha)

    # -----------------------------
    # GLOBAL SCORE (whole test)
    # -----------------------------
    global_llr = score_ids_llr(test_ids, probs_E, probs_S, V, alpha)
    print("\n=== GLOBAL TEST SCORE ===")
    print(f"LLR(test) = {global_llr:.3f}  (positive => Eminescu-like, negative => Stănescu-like)")

    # -----------------------------
    # SLIDING WINDOW SCAN
    # -----------------------------
    positions, scores = sliding_window_scan(
        test_ids, probs_E, probs_S, V, alpha,
        window_size=window_size, step=step
    )

    # -----------------------------
    # PLOT
    # -----------------------------
    plot_scan(
        positions, scores,
        title="Sliding window scan: Eminescu vs Nichita Stănescu (LLR)"
    )

    # Optional: print top few window decisions
    print("\n=== FIRST 10 WINDOWS (decision) ===")
    for i in range(min(10, len(scores))):
        who = "Eminescu" if scores[i] >= 0 else "Stănescu"
        print(f"window@{positions[i]:>5d}: score={scores[i]:>8.3f} -> {who}")

if __name__ == "__main__":
    main()
