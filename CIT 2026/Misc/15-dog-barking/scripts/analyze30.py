morse = ".-....-- .-..-..- .-.-.-.. .----.-- .--...-. ..--.-.. .---..-. .--.-.-- .--.-..- .--.---. .--..--- .-.----- .---.-.- .---.... .-.----- .---.-.. .--.-... ..--..-- .-.----- .---.--- .---..-. ..--.... .--.---. .--..--- .-.----- .---.-.. .---..-. ..--..-- ..--..-- .-----.-"

binary = morse.replace(".", "0").replace("-", "1")
print("Binary:", binary)

chars = []
for b in binary.split(" "):
    chars.append(chr(int(b, 2)))

print("Decoded:")
print("".join(chars))

# Try reverse mapping
binary2 = morse.replace(".", "1").replace("-", "0")
chars2 = []
for b in binary2.split(" "):
    chars2.append(chr(int(b, 2)))

print("Decoded (reverse):")
print("".join(chars2))
