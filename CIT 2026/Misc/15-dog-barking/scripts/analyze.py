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

# Find lengths of barking and silence
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

print("Events (state, length in 10ms units):")
print(events[:50])

# Try to decode as morse
morse = ""
for state, length in events:
    if state == 1:
        if length < 15:  # short bark
            morse += "."
        else:  # long bark
            morse += "-"
    elif length > 20 and length < 50:  # letter space
        morse += " "
    elif length >= 50:  # word space
        morse += " / "

print("\nMorse:")
print(morse)
