import random
import math
import collections

text = "GJZTYOZFYTccWBHFaBZYCcHFCFLPXQYHHQYaaODaaOTHWTRHaTYHWTFIHEGXYTcMWNLPDOPHHTUIHPbXGJZFGJZTYTccaNLPDQYHHOFHHZEaHODHHOFIHPSGYTLJWBQVaBHPEcZYCcHJCBZYKBQECKQXCAQTCAcPHAcPHAAGXNLXDJPaHTFHEQTaHQPaHZRaHQUIHTXUGaZHGaHHYOSKYTLTCFJJ"

# Simple bigram frequencies for English
bigrams = {
    'TH': 1.52, 'HE': 1.28, 'IN': 0.94, 'ER': 0.94, 'AN': 0.82, 'RE': 0.68,
    'ND': 0.63, 'AT': 0.59, 'ON': 0.57, 'NT': 0.56, 'HA': 0.56, 'ES': 0.56,
    'ST': 0.55, 'EN': 0.55, 'ED': 0.53, 'TO': 0.52, 'IT': 0.50, 'OU': 0.50,
    'EA': 0.47, 'HI': 0.46, 'IS': 0.46, 'OR': 0.43, 'TI': 0.34, 'AS': 0.33,
    'TE': 0.27, 'ET': 0.19, 'NG': 0.18, 'OF': 0.16, 'AL': 0.09, 'DE': 0.09,
    'SE': 0.08, 'LE': 0.08, 'SA': 0.06, 'SI': 0.05, 'AR': 0.04, 'VE': 0.04,
    'RA': 0.04, 'LD': 0.02, 'UR': 0.02
}

monograms = {
    'E': 12.7, 'T': 9.0, 'A': 8.1, 'O': 7.5, 'I': 6.9, 'N': 6.7, 'S': 6.3,
    'H': 6.0, 'R': 5.9, 'D': 4.2, 'L': 4.0, 'C': 2.7, 'U': 2.7, 'M': 2.4,
    'W': 2.3, 'F': 2.2, 'G': 2.0, 'Y': 1.9, 'P': 1.9, 'B': 1.4, 'V': 0.9,
    'K': 0.7, 'J': 0.1, 'X': 0.1, 'Q': 0.1, 'Z': 0.07, ' ': 19.0
}

def score(dec):
    s = 0
    for c in dec:
        s += math.log(monograms.get(c, 0.001))
    for i in range(len(dec)-1):
        bg = dec[i:i+2]
        s += math.log(bigrams.get(bg, 0.001))
    return s

unique_chars = list(set(text))
alphabet = " ETAOINSHRDLCUMWFGYPBVKJXQZ" + "".join(chr(i) for i in range(33, 127) if chr(i) not in " ETAOINSHRDLCUMWFGYPBVKJXQZ")

best_mapping = {c: alphabet[i] for i, c in enumerate(unique_chars)}
best_score = score("".join(best_mapping[c] for c in text))

T = 100.0
mapping = best_mapping.copy()
current_score = best_score

for i in range(100000):
    c1, c2 = random.sample(unique_chars, 2)
    mapping[c1], mapping[c2] = mapping[c2], mapping[c1]
    
    dec = "".join(mapping[c] for c in text)
    new_score = score(dec)
    
    if new_score > current_score or random.random() < math.exp((new_score - current_score) / T):
        current_score = new_score
        if new_score > best_score:
            best_score = new_score
            best_mapping = mapping.copy()
            if i % 10000 == 0:
                print(f"Score: {best_score}")
                print("".join(best_mapping[c] for c in text))
    else:
        mapping[c1], mapping[c2] = mapping[c2], mapping[c1]
        
    T *= 0.9999

print("Final:")
print("".join(best_mapping[c] for c in text))
