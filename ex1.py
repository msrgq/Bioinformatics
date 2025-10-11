# Find the percentage for all the dinucleotide and trinucleotide combinations for the sequence: S="ATTGTCCAATCTGTTG".

# 1. Build a brute force engine to generate all dinucleotide and trinucleotide combinations.
# 2. For each combination, find out the percentage inside the S sequence.
# 3. Show the percentage for each combination in the output of your implementation.

import itertools
import tkinter as tk
from tkinter import ttk, messagebox

def calculate_percentages():
    S = seq_entry.get().strip().upper()
    S = "".join([s for s in S if s in "ACGT"])

    if not S:
        messagebox.showerror("Error", "Please enter a valid DNA sequence (A, C, G, T).")
        return

    bases = ['A', 'C', 'G', 'T']
    results = []

    di_combos = [''.join(p) for p in itertools.product(bases, repeat=2)]
    di_counts = {combo: 0 for combo in di_combos}
    total_di = len(S) - 1 if len(S) > 1 else 0

    for i in range(total_di):
        dinuc = S[i:i+2]
        if dinuc in di_counts:
            di_counts[dinuc] += 1

    results.append("Dinucleotide Percentages:\n")
    results.append(f"{'Dinuc':<6}{'Count':>8}{'Percent':>12}")
    results.append("-" * 30)

    for combo in sorted(di_counts):
        percentage = (di_counts[combo] / total_di * 100) if total_di > 0 else 0
        results.append(f"{combo:<6}{di_counts[combo]:>8}{percentage:>11.2f}%")


    tri_combos = [''.join(p) for p in itertools.product(bases, repeat=3)]
    tri_counts = {combo: 0 for combo in tri_combos}
    total_tri = len(S) - 2 if len(S) > 2 else 0

    for i in range(total_tri):
        trinuc = S[i:i+3]
        if trinuc in tri_counts:
            tri_counts[trinuc] += 1

    results.append("\n\nTrinucleotide Percentages:\n")
    results.append(f"{'Trinuc':<6}{'Count':>8}{'Percent':>12}")
    results.append("-" * 30)

    for combo in sorted(tri_counts):
        percentage = (tri_counts[combo] / total_tri * 100) if total_tri > 0 else 0
        results.append(f"{combo:<6}{tri_counts[combo]:>8}{percentage:>11.2f}%")

    output_box.config(state="normal")
    output_box.delete("1.0", "end")
    output_box.insert("1.0", "\n".join(results))
    output_box.config(state="disabled")

root = tk.Tk()
root.title("Dinucleotide & Trinucleotide Percentage Calculator")
root.geometry("600x700")
root.resizable(False, False)

tk.Label(root, text="Enter DNA Sequence:", font=("Arial", 12, "bold")).pack(pady=10)

seq_entry = tk.Entry(root, width=50, font=("Arial", 12))
seq_entry.insert(0, "TACGTGCGCGCGAGCTATCTACTGACTTACGACTAGTGTAGCTGCATCATCGATCGA")
seq_entry.pack(pady=5)

calc_btn = tk.Button(root, text="Calculate Percentages",
                     command=calculate_percentages,
                     font=("Arial", 12, "bold"),
                     bg="#4CAF50", fg="white")
calc_btn.pack(pady=10)

frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill="both", expand=True)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side="right", fill="y")

output_box = tk.Text(frame, wrap="none", font=("Courier", 10),
                     bg="white", relief="solid", width=70, height=30,
                     yscrollcommand=scrollbar.set)
output_box.pack(side="left", fill="both", expand=True)
scrollbar.config(command=output_box.yview)
output_box.config(state="disabled")

root.mainloop()
