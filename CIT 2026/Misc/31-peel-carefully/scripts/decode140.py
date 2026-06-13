import math
import random
import collections
import urllib.request

# Download a short list of common English words to score the text
url = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt"
try:
    words = urllib.request.urlopen(url).read().decode('utf-8').split()
    word_set = set(words)
except:
    word_set = set(["the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it", "for", "not", "on", "with", "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up", "out", "if", "about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", "no", "just", "him", "know", "take", "people", "into", "year", "your", "good", "some", "could", "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", "think", "also", "back", "after", "use", "two", "how", "our", "work", "first", "well", "way", "even", "new", "want", "because", "any", "these", "give", "day", "most", "us", "flag", "cit"])

text = "啉鵴𓍯鵧啴鵴𓁥啥驷驲欠樵欳𒄠𓁯𓅴唬𓍢啴啉𓍧𓅥啳啉陷啳𓁷𐙯慧鸠啴陷啳樶栵挵㸍㸍繃𠅔ꔳ桢鑤ꍀ鑬𐘳散晤鱮𠌵"

# N-gram frequencies from a larger corpus would be better, but let's use a simple bigram/trigram model
bigrams = collections.defaultdict(float)
trigrams = collections.defaultdict(float)

# We can just use a generic English text to build the n-gram model
sample_text = "the quick brown fox jumps over the lazy dog. it was the best of times, it was the worst of times. the flag is cit{...} congratulations on solving this challenge. this is a very simple substitution cipher. we can use simulated annealing to solve it. the message reveals itself one layer at a time. it's all there just buried. can you read it?"
sample_text = "".join(c for c in sample_text.upper() if c.isalpha() or c == ' ')

for i in range(len(sample_text)-1):
    bigrams[sample_text[i:i+2]] += 1
for i in range(len(sample_text)-2):
    trigrams[sample_text[i:i+3]] += 1

def score(dec):
    s = 0
    words_in_dec = dec.split()
    for w in words_in_dec:
        if w.lower() in word_set:
            s += len(w) * 10
    for i in range(len(dec)-1):
        s += math.log10((bigrams[dec[i:i+2]] + 0.1) / len(sample_text))
    for i in range(len(dec)-2):
        s += math.log10((trigrams[dec[i:i+3]] + 0.1) / len(sample_text))
    return s

unique_chars = list(set(text))
alphabet = " ETAOINSHRDLCUMWFGYPBVKJXQZ" + "".join(chr(i) for i in range(33, 127) if chr(i) not in " ETAOINSHRDLCUMWFGYPBVKJXQZ")

best_mapping = {c: alphabet[i] for i, c in enumerate(unique_chars)}
best_mapping['啉'] = 'C'
best_mapping['鵴'] = 'I'
best_mapping['𓍯'] = 'T'
best_mapping['鵧'] = '{'
best_mapping['𠌵'] = '}'

best_score = score("".join(best_mapping[c] for c in text))

T = 100.0
mapping = best_mapping.copy()
current_score = best_score

fixed_chars = ['啉', '鵴', '𓍯', '鵧', '𠌵']

for i in range(100000):
    c1, c2 = random.sample(unique_chars, 2)
    if c1 in fixed_chars or c2 in fixed_chars:
        continue
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

