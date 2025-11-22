#Ex1 Make an artificial DNA sequence of 200-400b in length, in which to simulate 3-4 transposable elements.

import random

dna = "".join(random.choice("ACGT") for _ in range(300))
TEs = ["AAAACCCCTTTT", "GGGTTAGGGT", "CCCTAACCC", "TTAGGTTAA"]

chosen = random.sample(TEs, random.randint(3, 4))

for te in chosen:
    pos = random.randint(0, len(dna))
    dna = dna[:pos] + te + dna[pos:]

print(dna)
print("Length:", len(dna))
