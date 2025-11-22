#Ex2  Implement a software application to detect the positions of these transposable elements (start, end) within the created DNA sequence.

import random

dna = "".join(random.choice("ACGT") for _ in range(300))
TEs = ["AAAACCCCTTTT", "GGGTTAGGGT", "CCCTAACCC", "TTAGGTTAA"]

chosen = random.sample(TEs, random.randint(3, 4))
insert_positions = []
for te in chosen:
    pos = random.randint(0, len(dna))
    insert_positions.append((te, pos))
    dna = dna[:pos] + te + dna[pos:]

print("Final DNA sequence ({} bp):\n".format(len(dna)))
print(dna)

print("\nInserted transposons (sequence, start):")
for te, pos in insert_positions:
    print(te, pos)

def find_transposons(sequence, transposons):
    results = []
    for te in transposons:
        start = 0
        while True:
            idx = sequence.find(te, start)
            if idx == -1:
                break
            results.append((te, idx, idx + len(te)))
            start = idx + 1
    return results

detections = find_transposons(dna, TEs)

print("\nDetected transposons (sequence, start, end):")
for item in detections:
    print(item)

