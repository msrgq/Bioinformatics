#design an app that uses the sliding window method in order to read the tm over the sequence S. 
# use a sliding window f 8 positions and choose a FASTA file as input

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import math
import matplotlib.pyplot as plt


def read_fasta(filename):
    seq = ""
    with open(filename, 'r') as f:
        for line in f:
            if not line.startswith(">"):
                seq += line.strip().upper()
    return seq


def tm_basic(seq):
    G = seq.count('G')
    C = seq.count('C')
    A = seq.count('A')
    T = seq.count('T')
    return 4 * (G + C) + 2 * (A + T)


def tm_advanced(seq, na_conc=0.05):
    length = len(seq)
    if length == 0:
        return None
    gc_content = ((seq.count('G') + seq.count('C')) / length) * 100
    return 81.5 + 16.6 * math.log10(na_conc) + 0.41 * gc_content - (600 / length)


def sliding_window_tm(sequence, window_size=8, na_conc=0.05):
    results = []
    for i in range(len(sequence) - window_size + 1):
        window = sequence[i:i + window_size]
        tm_b = tm_basic(window)
        tm_a = tm_advanced(window, na_conc)
        results.append((i + 1, window, tm_b, tm_a))
    return results


class TMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DNA Melting Temperature (Tm) Calculator")
        self.root.geometry("750x550")
        self.root.configure(bg="#f9f9f9")

        self.filename = None
        self.sequence = ""

        ttk.Label(root, text="Sliding Window Tm Calculator", font=("Helvetica", 16, "bold")).pack(pady=10)

        frame = ttk.Frame(root)
        frame.pack(pady=5)

        ttk.Button(frame, text="Load FASTA File", command=self.load_fasta).grid(row=0, column=0, padx=5)
        ttk.Label(frame, text="Window size:").grid(row=0, column=1)
        self.window_entry = ttk.Entry(frame, width=5)
        self.window_entry.insert(0, "8")
        self.window_entry.grid(row=0, column=2, padx=5)

        ttk.Label(frame, text="[Na+] (M):").grid(row=0, column=3)
        self.na_entry = ttk.Entry(frame, width=7)
        self.na_entry.insert(0, "0.05")
        self.na_entry.grid(row=0, column=4, padx=5)

        ttk.Button(frame, text="Run", command=self.run_analysis).grid(row=0, column=5, padx=10)

        self.tree = ttk.Treeview(root, columns=("pos", "window", "tm_basic", "tm_adv"), show="headings", height=15)
        self.tree.heading("pos", text="Position")
        self.tree.heading("window", text="Window")
        self.tree.heading("tm_basic", text="Tm (Basic °C)")
        self.tree.heading("tm_adv", text="Tm (Advanced °C)")
        self.tree.column("pos", width=80)
        self.tree.column("window", width=150)
        self.tree.column("tm_basic", width=120)
        self.tree.column("tm_adv", width=130)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        ttk.Button(root, text="Show Graph", command=self.show_plot).pack(pady=5)

    def load_fasta(self):
        file_path = filedialog.askopenfilename(filetypes=[("FASTA files", "*.fasta *.fa *.txt")])
        if not file_path:
            return
        try:
            self.sequence = read_fasta(file_path)
            self.filename = file_path
            messagebox.showinfo("FASTA Loaded", f"Loaded sequence of length {len(self.sequence)} bases.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")

    def run_analysis(self):
        if not self.sequence:
            messagebox.showwarning("No Sequence", "Please load a FASTA file first.")
            return

        try:
            window_size = int(self.window_entry.get())
            na_conc = float(self.na_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Invalid window size or Na+ concentration.")
            return

        results = sliding_window_tm(self.sequence, window_size, na_conc)

        for row in self.tree.get_children():
            self.tree.delete(row)

        for pos, window, tm_b, tm_a in results:
            self.tree.insert("", tk.END, values=(pos, window, f"{tm_b:.2f}", f"{tm_a:.2f}"))

        self.results = results

    def show_plot(self):
        if not hasattr(self, "results") or not self.results:
            messagebox.showwarning("No Data", "Run the analysis first.")
            return

        positions = [r[0] for r in self.results]
        tm_b_vals = [r[2] for r in self.results]
        tm_a_vals = [r[3] for r in self.results]

        plt.figure(figsize=(10, 5))
        plt.plot(positions, tm_b_vals, label="Basic Tm (°C)", linestyle="--")
        plt.plot(positions, tm_a_vals, label="Advanced Tm (°C)")
        plt.title("Sliding Window Tm Profile")
        plt.xlabel("Position in Sequence")
        plt.ylabel("Melting Temperature (°C)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = TMApp(root)
    root.mainloop()
