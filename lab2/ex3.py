#find in sequence S only the dinucleodites and trinucleodites that exist, without the use of the brute force engine. 
# In order to achive the result one must verify each combination starting from the beggining of sequence S 
# Example: ABAA we have AB, BA, AA, ABA

def find_existing_kmers(S):
    S = S.upper().strip()

    dinucs = set()
    trinucs = set()

    for i in range(len(S)):
        if i + 1 < len(S):
            dinucs.add(S[i:i+2])
        if i + 2 < len(S):
            trinucs.add(S[i:i+3])

    return sorted(dinucs), sorted(trinucs)

S = "ABAA"
dinucs, trinucs = find_existing_kmers(S)

print(f"Sequence: {S}")
print(f"Existing dinucleotides (2-mers): {dinucs}")
print(f"Existing trinucleotides (3-mers): {trinucs}")