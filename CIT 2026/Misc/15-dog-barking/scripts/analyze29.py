import numpy as np
from scipy.io import wavfile

sample_rate, samples = wavfile.read("../files/challenge.wav")

if len(samples.shape) > 1:
    samples = samples[:, 0]

chunk_size = sample_rate // 100  # 10ms chunks
envelope = []
for i in range(0, len(samples), chunk_size):
    chunk = samples[i : i + chunk_size]
    envelope.append(np.max(np.abs(chunk)))

threshold = np.max(envelope) * 0.15
is_barking = [1 if e > threshold else 0 for e in envelope]

events = []
current_state = is_barking[0]
current_len = 0

for state in is_barking:
    if state == current_state:
        current_len += 1
    else:
        events.append((current_state, current_len))
        current_state = state
        current_len = 1
events.append((current_state, current_len))

words = []
current_pos = 0
for state, length in events:
    if state == 1:
        bark_samples = samples[
            current_pos * chunk_size : (current_pos + length) * chunk_size
        ]
        w = np.fft.fft(bark_samples)
        freqs = np.fft.fftfreq(len(w))
        peak_freq = abs(freqs[np.argmax(np.abs(w))]) * sample_rate

        if peak_freq < 500:
            words.append(".")
        elif peak_freq > 550:
            words.append("-")
        else:
            words.append(" ")
    current_pos += length

morse = "".join(words)
print("Morse:")
print(morse)

MORSE_CODE_DICT = {
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
    "-----": "0",
    "--..--": ",",
    ".-.-.-": ".",
    "..--..": "?",
    "-..-.": "/",
    "-....-": "-",
    "-.--.": "(",
    "-.--.-": ")",
}

decoded = ""
for word in morse.split(" "):
    if word in MORSE_CODE_DICT:
        decoded += MORSE_CODE_DICT[word]
    elif word == "":
        pass
    else:
        decoded += "?"

print("\nDecoded:")
print(decoded)
