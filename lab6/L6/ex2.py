import os
import glob
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from Bio import SeqIO

FASTA_DIR = "C:/Users/msuru/Desktop/BIOINF/lab6/influenza_fastas"
OUTPUT_DIR = "C:/Users/msuru/Desktop/BIOINF/lab6/gel_outputs" 
ENZYME_SITE = "GAATTC"         
K = 1000.0
ALPHA = 1.0
MAX_LANE_WIDTH = 0.6

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "separate_gels"), exist_ok=True)

def read_and_concatenate_fasta(fasta_path):

    seqs = []
    for rec in SeqIO.parse(fasta_path, "fasta"):
        seqs.append(str(rec.seq).upper())
    concatenated = "".join(seqs)
    return concatenated

def digest_sequence(seq, site):

    if len(site) == 0:
        raise ValueError("Enzyme site must be non-empty.")
    parts = seq.split(site)
    lengths = [len(p) for p in parts if len(p) > 0]
    return lengths

def simulate_migration(lengths, K=K, alpha=ALPHA):
    return [K / (l ** alpha) for l in lengths]

def plot_single_lane(ax, fragment_lengths, migrations, lane_center_x=1.0, color='tab:blue', label=None):
    x0 = lane_center_x - MAX_LANE_WIDTH
    x1 = lane_center_x + MAX_LANE_WIDTH
    pairs = sorted(zip(fragment_lengths, migrations), key=lambda p: p[1])
    for (length, dist) in pairs:
        ax.hlines(y=dist, xmin=x0, xmax=x1, linewidth=8, color=color, alpha=0.8)
        ax.text(x1 + 0.08, dist, f"{length} bp", va='center', fontsize=7)

    if label:
        ax.text(lane_center_x, ax.get_ylim()[1] + 0.1 * (ax.get_ylim()[1] - ax.get_ylim()[0]),
                label, ha='center', va='bottom', fontsize=8, rotation=90)

fasta_paths = sorted(glob.glob(os.path.join(FASTA_DIR, "*.fasta")) + glob.glob(os.path.join(FASTA_DIR, "*.fa")))
if len(fasta_paths) == 0:
    raise RuntimeError(f"No FASTA files found in directory '{FASTA_DIR}'. Place your 10 fasta files there (extension .fasta or .fa).")
fasta_paths = fasta_paths[:10]
print(f"Found {len(fasta_paths)} FASTA files. Using these files:")
for p in fasta_paths:
    print(" -", os.path.basename(p))

results = []
for path in fasta_paths:
    name = os.path.basename(path)
    seq = read_and_concatenate_fasta(path)
    seq_len = len(seq)
    frag_lengths = digest_sequence(seq, ENZYME_SITE)
    migrations = simulate_migration(frag_lengths, K=K, alpha=ALPHA)

    results.append({
        "filename": name,
        "seq_len": seq_len,
        "fragment_lengths": frag_lengths,
        "migrations": migrations,
        "n_fragments": len(frag_lengths)
    })

most = max(results, key=lambda r: r["n_fragments"])
print("\nSummary of fragments per genome:")
for r in results:
    print(f" {r['filename']}: total_length={r['seq_len']} bp, fragments={r['n_fragments']}")

print(f"\nGenome with the most fragments: {most['filename']} ({most['n_fragments']} fragments)")

fig_width = max(6, len(results) * 0.8)
fig, ax = plt.subplots(figsize=(fig_width, 8))

all_migrations = [m for r in results for m in r['migrations']]
if len(all_migrations) == 0:
    raise RuntimeError("No fragments computed (unexpected). Check your sequences or enzyme site.")
y_min = 0
y_max = max(all_migrations) * 1.15

for i, r in enumerate(results):
    lane_x = i + 1
    color = plt.cm.tab10(i % 10)
    plot_single_lane(ax, r['fragment_lengths'], r['migrations'], lane_center_x=lane_x, color=color, label=r['filename'])

ax.set_xlim(0.5, len(results) + 0.5)
ax.set_ylim(y_max, y_min)
ax.invert_yaxis()
ax.set_xticks([i+1 for i in range(len(results))])
ax.set_xticklabels([os.path.splitext(r['filename'])[0] for r in results], rotation=90, fontsize=8)
ax.set_ylabel("Migration distance (arb. units)")
ax.set_title(f"Simulated EcoRI (GAATTC) digestion - Combined gel for {len(results)} genomes")
plt.tight_layout()
combined_path = os.path.join(OUTPUT_DIR, "combined_gel.png")
plt.savefig(combined_path, dpi=300)
print(f"Saved combined gel to: {combined_path}")
plt.show()
for r in results:
    fig, ax = plt.subplots(figsize=(3, 6))
    ax.set_ylim(y_max, y_min)
    ax.invert_yaxis()
    plot_single_lane(ax, r['fragment_lengths'], r['migrations'], lane_center_x=1.0, color='tab:blue', label=r['filename'])
    ax.set_xlim(0.5, 1.5)
    ax.set_xticks([])
    ax.set_ylabel("Migration distance (arb. units)")
    ax.set_title(r['filename'])
    plt.tight_layout()
    outfn = os.path.join(OUTPUT_DIR, "separate_gels", f"{os.path.splitext(r['filename'])[0]}_gel.png")
    plt.savefig(outfn, dpi=300)
    plt.close(fig)

print(f"Saved separate gel images to: {os.path.join(OUTPUT_DIR, 'separate_gels')}")

names = [r['filename'] for r in results]
counts = [r['n_fragments'] for r in results]

fig, ax = plt.subplots(figsize=(max(6, len(results) * 0.6), 4))
ax.bar(range(len(names)), counts, color=[plt.cm.tab10(i % 10) for i in range(len(names))])
ax.set_xticks(range(len(names)))
ax.set_xticklabels([os.path.splitext(n)[0] for n in names], rotation=45, ha='right', fontsize=9)
ax.set_ylabel("Fragment count after EcoRI digestion")
ax.set_title("Number of fragments per genome (EcoRI)")
plt.tight_layout()
bar_path = os.path.join(OUTPUT_DIR, "fragment_counts.png")
plt.savefig(bar_path, dpi=300)
plt.show()
print(f"Saved fragment counts bar chart to: {bar_path}")

summary_path = os.path.join(OUTPUT_DIR, "summary.txt")
with open(summary_path, "w") as fh:
    fh.write("Filename\tTotal_length_bp\tNum_fragments\n")
    for r in results:
        fh.write(f"{r['filename']}\t{r['seq_len']}\t{r['n_fragments']}\n")
print(f"Saved summary to: {summary_path}")
print("\nDone. Outputs saved in:", OUTPUT_DIR)
