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

barks = [length for state, length in events if state == 1]
silences = [length for state, length in events if state == 0]

print("Barks:", sorted(list(set(barks))))
print("Silences:", sorted(list(set(silences))))
