import numpy as np
from scipy.io import wavfile

sample_rate, samples = wavfile.read("../files/challenge.wav")

if len(samples.shape) > 1:
    samples = samples[:, 0]

# Simple envelope detection
chunk_size = sample_rate // 100  # 10ms chunks
envelope = []
for i in range(0, len(samples), chunk_size):
    chunk = samples[i : i + chunk_size]
    envelope.append(np.max(np.abs(chunk)))

threshold = np.max(envelope) * 0.3
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

clusters = []
current_cluster = 0
for state, length in events:
    if state == 1:
        current_cluster += 1
    elif length > 10:
        if current_cluster > 0:
            clusters.append(current_cluster)
        current_cluster = 0
if current_cluster > 0:
    clusters.append(current_cluster)

print("Barks per cluster:")
print(clusters)

# Try to map to ASCII
ascii_str = "".join(chr(c) for c in clusters if c < 128)
print("\nASCII:")
print(ascii_str)

# Try to map to A1Z26
a1z26 = "".join(chr(c + ord("a") - 1) if 1 <= c <= 26 else "?" for c in clusters)
print("\nA1Z26:")
print(a1z26)
