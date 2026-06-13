# Try to read the wave file and see if we can find morse or just generate a spectrogram
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile

sample_rate, samples = wavfile.read("../files/challenge.wav")
frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)

plt.pcolormesh(times, frequencies, spectrogram)
plt.ylabel("Frequency [Hz]")
plt.xlabel("Time [sec]")
plt.savefig("spectrogram.png")
