#use AI to adapt your current algorithm in order to make an app that takes a FASTA file and reads the seq content from it and displays the relative percentages for the symbols present in the alphabet of the sequence
#note that FASTA reoresents a file format that contains DNA, ARN or protein sequences
#thus,it contains information for your input.

filename = "C:/Users/msuru/Desktop/BIOINF/lab1/sequence.fasta"  

with open(filename, "r") as f:
    lines = f.readlines()

S = "".join([line.strip() for line in lines if not line.startswith(">")]).upper()
n = len(S)

alphabet = set(S)

print("Sequence length:", n)
print("Alphabet found in sequence with percentages:")

for letter in sorted(alphabet):
    count = S.count(letter)
    percentage = round((count / n) * 100)
    print(letter, ":", percentage, "%")