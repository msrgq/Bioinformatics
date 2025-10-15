#The melting temperature (Tm) is the temperature at which one-half of a particular DNA duplex will dissociate and become a single strand of DNA. 
# Primer length and sequence are of critical importance in designing the parameters of a successful amplification. 
# The melting temperature of a nucleic acid duplex increases both with its length, and with increasing GC content. 
# A simple formula for calculation of the (Tm) is:  Tm = 4(G + C) + 2(A + T) °C 
# The actual Tm is influenced by the concentration of Mg2+ , K+ , and cosolvents. An alternative formula is:
# Tm = 81.5 + 16.6(log10([Na+])) + .41*(%GC) – 600/length.
# Implement an application that calculates the melting temperature of a DNA sequence using one of these formulas or both. Input = a string of DNA, Output = temperature in celsius

import math

def calculate_tm_basic(dna_sequence):
    dna_sequence = dna_sequence.upper()
    G = dna_sequence.count('G')
    C = dna_sequence.count('C')
    A = dna_sequence.count('A')
    T = dna_sequence.count('T')
    tm = 4 * (G + C) + 2 * (A + T)
    return tm

def calculate_tm_advanced(dna_sequence, na_conc=0.05):
    dna_sequence = dna_sequence.upper()
    length = len(dna_sequence)
    if length == 0:
        return None 

    gc_content = ((dna_sequence.count('G') + dna_sequence.count('C')) / length) * 100
    tm = 81.5 + 16.6 * math.log10(na_conc) + 0.41 * gc_content - (600 / length)
    return tm

if __name__ == "__main__":
    dna = input("Enter a DNA sequence: ").strip()

    tm_basic = calculate_tm_basic(dna)
    tm_advanced = calculate_tm_advanced(dna)

    print(f"\nDNA Sequence: {dna}")
    print(f"Length: {len(dna)} bases")
    print(f"Basic Formula Tm: {tm_basic:.2f} °C")
    print(f"Advanced Formula Tm: {tm_advanced:.2f} °C")
