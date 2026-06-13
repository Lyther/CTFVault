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

barks = []
current_pos = 0
for state, length in events:
    if state == 1:
        bark_samples = samples[
            current_pos * chunk_size : (current_pos + length) * chunk_size
        ]
        w = np.fft.fft(bark_samples)
        freqs = np.fft.fftfreq(len(w))
        peak_freq = abs(freqs[np.argmax(np.abs(w))]) * sample_rate
        barks.append(int(round(peak_freq)))
    current_pos += length


def classify_freq(f):
    if 450 < f < 500:
        return "A"
    if 500 < f < 550:
        return "B"
    if 550 < f < 595:
        return "C"
    if 595 < f < 650:
        return "D"
    if 800 < f < 900:
        return "E"
    if 1300 < f < 1500:
        return "F"
    return "?"


clusters = []
current_cluster = []
bark_idx = 0
for state, length in events:
    if state == 1:
        current_cluster.append(classify_freq(barks[bark_idx]))
        bark_idx += 1
    elif length > 10:
        if current_cluster:
            clusters.append("".join(current_cluster))
        current_cluster = []
if current_cluster:
    clusters.append("".join(current_cluster))

print("Clusters:")
print(" ".join(clusters))
