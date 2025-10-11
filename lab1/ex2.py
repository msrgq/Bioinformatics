#A DNA seq is given: S = 'ACGGGCATATGCGC"/\. Make an app which is able to show the percentage of the components frpm the alphabet of seq S.
#in other words, the input of the seq S and the output is the alphabet of the seq and the percentage of each letter in the alphabet found in seq S.

s = "ACGGGCATATGCGC"
n = len(s)
alphabet = set(s)

for letter in alphabet:
    count = s.count(letter)
    percentage = (count/n) * 100
    print(letter, ":", percentage, "%")
