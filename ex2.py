#Design an application using AI, which contains a GUI which allows the user to choose a FASTA file. The content of the file should be analysed by using a sliding window of 30 positions. 
#The content for each sliding window should be used in order to extract the relative freqs of the symbols found in the alphabet of the seq. 
# Thus, your input should be the DNA sequence from the fasta file and the output should be the values of the relative freqs of each symbol from the seq translated as lines on a chart. 
# Thus, your chart in the case of DNA should have 4 lines which reflect the values found over the seq

import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt

def read_fasta(path):
    seq = ""
    with open(path, "r") as f:
        for line in f:
            if not line.startswith(">"):
                seq += line.strip().upper()
    return seq

def analyze_sequence(seq, window=30):
    if len(seq) < window:
        return [], {b: [] for b in "ACGT"}

    positions = []
    freqs = {b: [] for b in "ACGT"}
    for i in range(len(seq) - window + 1):
        w = seq[i:i+window]
        total = len(w)
        for b in "ACGT":
            freqs[b].append(w.count(b)/total)
        positions.append(i+1)
    return positions, freqs

def choose_file():
    path = filedialog.askopenfilename(
        title="Select FASTA File",
        filetypes=[("FASTA files", "*.fasta *.fa *.txt"), ("All files", "*.*")]
    )
    if not path:
        return
    seq = read_fasta(path)
    if not seq:
        messagebox.showerror("Error", "No valid DNA sequence found!")
        return
    positions, freqs = analyze_sequence(seq, 30)
    if not positions:
        messagebox.showinfo("Info", "Sequence shorter than 30 bases.")
        return

    plt.figure(figsize=(8,4))
    for b in "ACGT":
        plt.plot(positions, freqs[b], label=b)
    plt.xlabel("Window start position")
    plt.ylabel("Relative frequency")
    plt.title("Sliding Window (30) – DNA Base Frequencies")
    plt.ylim(0,1)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

root = tk.Tk()
root.title("DNA Frequency Analyzer")
root.geometry("400x200")

tk.Label(root, text="DNA Sliding Window Frequency Analyzer",
         font=("Arial", 12, "bold")).pack(pady=20)

tk.Button(root, text="Choose FASTA File",
          font=("Arial", 12),
          command=choose_file,
          bg="#4CAF50", fg="white").pack(pady=10)

tk.Label(root, text="Window size = 30 bases", font=("Arial", 10)).pack(pady=5)

root.mainloop()
