import math
from typing import Dict, Tuple, List

BASES = "ACGT"
IDX = {b: i for i, b in enumerate(BASES)}

def count_transitions(seq: str) -> List[List[int]]:

    seq = seq.strip().upper()
    counts = [[0 for _ in BASES] for _ in BASES]

    for a, b in zip(seq, seq[1:]):
        if a not in IDX or b not in IDX:
            raise ValueError(f"Invalid DNA character in sequence: {a}->{b}")
        counts[IDX[a]][IDX[b]] += 1

    return counts

def row_normalize(counts: List[List[int]]) -> List[List[float]]:
    probs = [[0.0 for _ in BASES] for _ in BASES]
    for i in range(4):
        row_sum = sum(counts[i])
        if row_sum == 0:
            continue
        for j in range(4):
            probs[i][j] = counts[i][j] / row_sum
    return probs

def log_likelihood_matrix(tr_plus: List[List[float]],
                          tr_minus: List[List[float]],
                          eps: float = 1e-17) -> List[List[float]]:
    llm = [[0.0 for _ in BASES] for _ in BASES]
    for i in range(4):
        for j in range(4):
            p = tr_plus[i][j] + eps
            q = tr_minus[i][j] + eps
            llm[i][j] = math.log(p / q, 2)
    return llm

def score_sequence(seq: str, llm: List[List[float]]) -> float:
    seq = seq.strip().upper()
    total = 0.0
    for a, b in zip(seq, seq[1:]):
        total += llm[IDX[a]][IDX[b]]
    return total

def pretty_print_matrix(mat, title: str, fmt: str = "{:8.3f}") -> None:
    print(f"\n{title}")
    print("     " + " ".join([f"{b:>8s}" for b in BASES]))
    for i, r in enumerate(mat):
        row_label = BASES[i]
        print(f"{row_label:>3s} " + " ".join(fmt.format(x) for x in r))

def pretty_print_counts(mat, title: str) -> None:
    print(f"\n{title}")
    print("     " + " ".join([f"{b:>5s}" for b in BASES]))
    for i, r in enumerate(mat):
        row_label = BASES[i]
        print(f"{row_label:>3s} " + " ".join(f"{x:5d}" for x in r))

if __name__ == "__main__":
    S1 = "ATCGATTCGATATCATACACGTAT" 
    S2 = "CTCGACTAGTATGAAGTCCACGCTTG" 
    S  = "CAGGTTGGAAACGTAA"

    c_plus  = count_transitions(S1)
    c_minus = count_transitions(S2)

    tr_plus  = row_normalize(c_plus)
    tr_minus = row_normalize(c_minus)
    llm = log_likelihood_matrix(tr_plus, tr_minus, eps=1e-17)

    pretty_print_counts(c_plus,  "Transition COUNTS (+) from S1")
    pretty_print_counts(c_minus, "Transition COUNTS (-) from S2")

    pretty_print_matrix(tr_plus,  "Transition PROBS Tr(+) from S1", fmt="{:8.6f}")
    pretty_print_matrix(tr_minus, "Transition PROBS Tr(-) from S2", fmt="{:8.6f}")

    pretty_print_matrix(llm, "Log-Likelihood Matrix LLM = log2(Tr+/Tr-)")

    total_score = score_sequence(S, llm)
    print(f"\nSequence S = {S}")
    print(f"Total log-likelihood score = {total_score:.6f}")

    if total_score > 0:
        print("Decision: CpG ISLAND (+)")
    else:
        print("Decision: NON-ISLAND (-)")
