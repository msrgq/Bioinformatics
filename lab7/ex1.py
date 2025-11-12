#1. Take an arbitrary DNA sequence from the NCBI (National Center for Biotechnology), between 1000 and 3000 nucleotides (letters).
# 2. Implement a software application that detects repetitions (between 6b and 10b) in this DNA sequence. 
# 3.Plot the sequence of the repetitions found.
# 4. Download 10 influenza genoms. For each, plot the frequences of found repetitions.

import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

def read_fasta(filepath):
    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if not line.startswith(">")]
    return "".join(lines).upper()

def find_repeats(seq, min_len=6, max_len=10):
    repeats = {}
    for length in range(min_len, max_len + 1):
        seen = {}
        for i in range(len(seq) - length + 1):
            subseq = seq[i:i + length]
            seen.setdefault(subseq, 0)
            seen[subseq] += 1
        for subseq, count in seen.items():
            if count > 1:
                repeats[subseq] = count
    return repeats

def plot_repeats_on_ax(repeats, genome_name, ax, top_n=20):
    if not repeats:
        ax.text(0.5, 0.5, "No repeats", ha='center', va='center')
        ax.set_title(genome_name)
        ax.axis("off")
        return

    sorted_repeats = sorted(repeats.items(), key=lambda x: x[1], reverse=True)[:top_n]
    subseqs = [s for s, _ in sorted_repeats]
    counts = [c for _, c in sorted_repeats]

    ax.bar(subseqs, counts)
    ax.set_title(f"DNA Repeats Frequency — {genome_name}", fontsize=10)
    ax.set_xlabel("Repeated subsequences (6–10 bases)", fontsize=8)
    ax.set_ylabel("Number of occurrences", fontsize=8)
    ax.set_xticklabels(subseqs, rotation=90, fontsize=8)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    fasta_paths = filedialog.askopenfilenames(
        title="Select FASTA files for influenza genomes",
        filetypes=[("FASTA files", "*.fasta *.fa *.fna"), ("All files", "*.*")]
    )

    if not fasta_paths:
        print("No files selected")
        exit()

    print(f"Selected {len(fasta_paths)} genome files")

    all_repeats = []
    genome_names = []

    for path in fasta_paths:
        genome_name = path.split("/")[-1].split("\\")[-1]
        genome_names.append(genome_name)

        print(f"\nProcessing {genome_name}...")
        dna = read_fasta(path)
        repeats = find_repeats(dna)
        all_repeats.append(repeats)

        print(f"  Found {len(repeats)} repeated subsequences")
        for subseq, count in sorted(repeats.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"    {subseq} -> {count} times")

    num_genomes = len(all_repeats)
    cols = 2
    rows = (num_genomes + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(12, 6*rows))
    axes = axes.flatten()

    for i, repeats in enumerate(all_repeats):
        plot_repeats_on_ax(repeats, genome_names[i], axes[i])

    for j in range(i+1, len(axes)):
        axes[j].axis("off")

    plt.tight_layout()
    plt.show()
