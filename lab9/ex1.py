#. Take an arbitrary DNA sequence from the NCBI (National Center for Biotechnology), between 1000 and 3000 nucleotides (letters). 
# 2. Use 5 restriction enzymes (enzyme name, recognized sequence, cleavage site):   	

enzymes = [
    {"name": "EcoRI", "recognition": "GAATTC", "cut_index": 1},
    {"name": "BamHI", "recognition": "GGATCC", "cut_index": 1},
    {"name": "HindIII", "recognition": "AAGCTT", "cut_index": 1},
    {"name": "TaqI", "recognition": "TCGA", "cut_index": 1}, 
    {"name": "HaeIII", "recognition": "GGCC", "cut_index": 2} 
]

dna_sequence = """
GCGCCCAATACGCAAACCGCCTCTCCCCGCGCGTTGGCCGATTCATTAATGCAGCTGGCA
CGACAGGTTTCCCGACTGGAAAGCGGGCAGTGAGCGCAACGCAATTAATGTGAGTTAGCT
CACTCATTAGGCACCCCAGGCTTTACACTTTATGCTTCCGGCTCGTATGTTGTGTGGAAT
TGTGAGCGGATAACAATTTCACACAGGAAACAGCTATGACCATGATTACGCCAAGCTTGC
ATGCCTGCAGGTCGACTCTAGAGGATCCCCGGGTACCGAGCTGAATTCACTGGCCGTCG
TTTTACAACGTCGTGACTGGGAAAACCCTGGCGTTACCCAACTTAATCGCCTTGCAGCAC
""".replace("\n", "")

def find_cuts(dna, recognition, cut_index):
    positions = []
    start = 0
    while True:
        idx = dna.find(recognition, start)
        if idx == -1:
            break
        positions.append(idx + cut_index)
        start = idx + 1
    return positions

def digest(dna, enzymes):
    cut_sites = {}
    for enzyme in enzymes:
        cuts = find_cuts(dna, enzyme["recognition"], enzyme["cut_index"])
        cut_sites[enzyme["name"]] = cuts
    return cut_sites

def fragment_sizes(dna, cut_positions):
    cuts = sorted(cut_positions)
    if not cuts:
        return [len(dna)]
    fragments = []
    prev = 0
    for cut in cuts:
        fragments.append(cut - prev)
        prev = cut
    fragments.append(len(dna) - prev)
    return fragments

def ascii_gel(fragments):
    fragments_sorted = sorted(fragments, reverse=True)
    max_len = max(fragments_sorted)
    print("Simulated Gel (top -> large, bottom -> small):")
    for f in fragments_sorted:
        bar_length = max(1, int(f / max_len * 50)) 
        print(f"{f:>5} bp | " + "="*bar_length)


cut_sites = digest(dna_sequence, enzymes)

print("Cleavage positions:")
all_cuts = []
for enzyme, cuts in cut_sites.items():
    print(f"{enzyme}: {len(cuts)} cuts at positions {cuts}")
    all_cuts.extend(cuts)

fragments = fragment_sizes(dna_sequence, all_cuts)
print("\nFragment sizes (bp):", fragments)
print()
ascii_gel(fragments)
