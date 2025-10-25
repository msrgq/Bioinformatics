#download from NCBI the FASTA files containing the COVID-19 genome and the influenza genome. use AI to compare the codon frequencies between the two. 
#a) make a chart that shows the top 10 most frequent codons for COVID-19. 
#b)make a chart that shows the top 10 most frequent codons for influenza 
#c)compare the two results and show the most frequent codons between the two d)show in the output of the console top 3 amino acids for each genome

import matplotlib.pyplot as plt
from collections import Counter
import matplotlib

genetic_code = {
    'UUU':'F','UUC':'F','UUA':'L','UUG':'L','CUU':'L','CUC':'L','CUA':'L','CUG':'L',
    'AUU':'I','AUC':'I','AUA':'I','AUG':'M','GUU':'V','GUC':'V','GUA':'V','GUG':'V',
    'UCU':'S','UCC':'S','UCA':'S','UCG':'S','CCU':'P','CCC':'P','CCA':'P','CCG':'P',
    'ACU':'T','ACC':'T','ACA':'T','ACG':'T','GCU':'A','GCC':'A','GCA':'A','GCG':'A',
    'UAU':'Y','UAC':'Y','UAA':'Stop','UAG':'Stop','CAU':'H','CAC':'H','CAA':'Q','CAG':'Q',
    'AAU':'N','AAC':'N','AAA':'K','AAG':'K','GAU':'D','GAC':'D','GAA':'E','GAG':'E',
    'UGU':'C','UGC':'C','UGA':'Stop','UGG':'W','CGU':'R','CGC':'R','CGA':'R','CGG':'R',
    'AGU':'S','AGC':'S','AGA':'R','AGG':'R','GGU':'G','GGC':'G','GGA':'G','GGG':'G'
}

def read_fasta(filepath):
    """Read a FASTA file and return the concatenated sequence."""
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if not line.startswith('>')]
    seq = ''.join(lines).upper().replace('T', 'U')  # DNA → RNA
    return seq

def codon_frequency(sequence):
    """Count codon frequencies from an RNA sequence."""
    codons = [sequence[i:i+3] for i in range(0, len(sequence) - 2, 3)]
    codons = [c for c in codons if len(c) == 3]
    return Counter(codons)

def amino_acid_frequency(codon_counts):
    """Count amino acid frequencies from codon counts."""
    aa_counts = Counter()
    for codon, count in codon_counts.items():
        aa = genetic_code.get(codon, '?')
        if aa not in ['Stop', '?']:
            aa_counts[aa] += count
    return aa_counts

def plot_top_codons(codon_counts, title, savefile=None):
    """Plot top 10 codons."""
    top_codons = codon_counts.most_common(10)
    codons, freqs = zip(*top_codons)
    plt.bar(codons, freqs)
    plt.title(title)
    plt.xlabel("Codon")
    plt.ylabel("Frequency")
    plt.tight_layout()
    if savefile:
        plt.savefig(savefile)
    else:
        plt.show()

covid_fasta = "C:/Users/msuru/Desktop/BIOINF/lab4/covid_genome.fasta"    
flu_fasta = "C:/Users/msuru/Desktop/BIOINF/lab4/influenza_genome.fasta"

covid_seq = read_fasta(covid_fasta)
flu_seq = read_fasta(flu_fasta)

covid_codons = codon_frequency(covid_seq)
flu_codons = codon_frequency(flu_seq)

plot_top_codons(covid_codons, "Top 10 Codons - COVID-19", "covid_codons.png")
plt.show()
plot_top_codons(flu_codons, "Top 10 Codons - Influenza", "influenza_codons.png")
plt.show()

covid_top = set([codon for codon, _ in covid_codons.most_common(10)])
flu_top = set([codon for codon, _ in flu_codons.most_common(10)])
common_codons = covid_top & flu_top
print("Common frequent codons:", common_codons)

covid_aa = amino_acid_frequency(covid_codons)
flu_aa = amino_acid_frequency(flu_codons)

print("\nTop 3 amino acids - COVID-19:")
for aa, count in covid_aa.most_common(3):
    print(f"{aa}: {count}")

print("\nTop 3 amino acids - Influenza:")
for aa, count in flu_aa.most_common(3):
    print(f"{aa}: {count}")
