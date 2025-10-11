#make an application that is able to find the alphabet of a sequence of text. this seq may be an ARN seq or ADN seq or protein seq

s = "ABACTGSAJLJJSM"
n = len(s)
alphabet = set(s)

for letter in alphabet:
    print(letter)
