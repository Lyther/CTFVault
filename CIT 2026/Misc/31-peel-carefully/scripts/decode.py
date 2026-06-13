import sys

morse_dict = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F',
    '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
    '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
    '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
    '-.--': 'Y', '--..': 'Z', '-----': '0', '.----': '1', '..---': '2',
    '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
    '---..': '8', '----.': '9', '.-.-.-': '.', '--..--': ',', '..--..': '?',
    '.----.': "'", '-.-.--': '!', '-..-.': '/', '-.--.': '(', '-.--.-': ')',
    '.-...': '&', '---...': ':', '-.-.-.': ';', '-...-': '=', '.-.-.': '+',
    '-....-': '-', '..--.-': '_', '.-..-.': '"', '...-..-': '$', '.--.-.': '@'
}

with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/challenge.txt", "r") as f:
    data = f.read().strip()

words = data.split(' ')
decoded = ""
for w in words:
    if w in morse_dict:
        decoded += morse_dict[w]
    elif w == '':
        decoded += ' '
    else:
        decoded += '?'

print(decoded[:100])
with open("/Users/bytedance/Documents/CTF/CIT 2026/Misc/31-peel-carefully/files/layer1.txt", "w") as f:
    f.write(decoded)
