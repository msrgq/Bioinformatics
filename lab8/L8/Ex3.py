#Ex3 Download from NCBI 3 bacterial genoms of your choosing. 
#try to find in these genoms possible transposons. for this one must detect possible inverted repeats without prior knowledge about their existance in the sequence.
#the inverted repeat should have a min length of 4 letters and a max of 6 letters.

import tkinter as tk
from tkinter import filedialog, messagebox

def reverse_complement(seq):
    comp = str.maketrans("ATGC", "TACG")
    return seq.translate(comp)[::-1]

def load_fasta(path):
    seq = []
    with open(path, "r") as f:
        for line in f:
            if not line.startswith(">"):
                seq.append(line.strip().upper())
    return "".join(seq)

def find_inverted_repeats(genome, min_len=4, max_len=6, max_spacer=500):

    results = []
    n = len(genome)

    for arm_len in range(min_len, max_len + 1):

        for i in range(n - arm_len):
            left = genome[i:i + arm_len]
            rc_left = reverse_complement(left)

            start_search = i + arm_len

            max_right_pos = min(n - arm_len, i + arm_len + max_spacer)

            for j in range(start_search, max_right_pos + 1):
                right = genome[j:j + arm_len]

                if right == rc_left:
                    results.append({
                        "arm_length": arm_len,
                        "repeat": left,
                        "left_start": i,
                        "left_end": i + arm_len - 1,
                        "right_start": j,
                        "right_end": j + arm_len - 1,
                        "spacer": j - (i + arm_len)
                    })

    return results


def open_file():
    filepath = filedialog.askopenfilename(
        title="Select Genome FASTA File",
        filetypes=[("FASTA files", "*.fasta *.fa *.fna"), ("All files", "*.*")]
    )

    if not filepath:
        return

    messagebox.showinfo("Loading", f"Loading genome:\n{filepath}")

    try:
        genome = load_fasta(filepath)
    except Exception as e:
        messagebox.showerror("Error", f"Could not read file:\n{e}")
        return

    print("Genome loaded. Length:", len(genome), "bp")
    print("Detecting inverted repeats (4–6 bp, spacer ≤ 500 bp)...")

    hits = find_inverted_repeats(genome)

    print("Found:", len(hits), "inverted repeats")

    out_file = filepath + "_inverted_repeats.txt"
    with open(out_file, "w") as f:
        f.write("arm_length\trepeat\tleft_start\tleft_end\tright_start\tright_end\tspacer\n")
        for h in hits:
            f.write(
                f"{h['arm_length']}\t{h['repeat']}\t"
                f"{h['left_start']}\t{h['left_end']}\t"
                f"{h['right_start']}\t{h['right_end']}\t"
                f"{h['spacer']}\n"
            )

    messagebox.showinfo(
        "Done",
        f"Found {len(hits)} inverted repeats.\n\n"
        f"Results saved to:\n{out_file}"
    )


# GUI
root = tk.Tk()
root.title("Transposon Finder – Inverted Repeat Detector")
root.geometry("420x200")

label = tk.Label(root, text="Select a bacterial genome FASTA file", font=("Arial", 12))
label.pack(pady=20)

btn = tk.Button(root, text="Choose File", command=open_file, font=("Arial", 12))
btn.pack(pady=20)

root.mainloop()
