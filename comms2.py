import matplotlib.pyplot as plt
import numpy as np
from math import pi
plt.close('all')
# Set basic params
fs = 4096e6 # sample rate
fb = 64e6 # frequency of baseband signal
A = 2 # baseband signal amplitude
N_fft = 2048 # fft size

t = np.arange(N_fft)/fs #time scale
# Define input signal
g = A*np.cos(2*np.pi*fb*t) 
# Calculate FFT
g_fft_result = np.fft.fft(g, N_fft)

# Get the corresponding frequencies, that depend on N_fft and Fs - freq. domain x axis
freqs = np.fft.fftfreq(N_fft,1/fs)  

def binary(sym, sym_len):
  rand_n = np.random.rand(sym)
  rand_n[np.where(rand_n >= 0.5)] = 1
  rand_n[np.where(rand_n <= 0.5)] = 0

  sig = np.zeros(int(sym*sym_len))

  # generating symbols
  id1 = np.where(rand_n == 1)

  for i in id1[0]:
    temp = int(i*sym_len)
    sig[temp:temp+sym_len] = 1
  return sig

# Carrier wave and binary waveform configuration parameters
Fs = 1e6 # Samples per second
fc = 915e6  # Carrier frequency 100 Hz, 100 cycles/sec
T = 1 # Total simulation time in seconds
t = np.arange(0, T, 1/Fs)
x =np.sin(2*pi*fc*t)
Td = 0.1 # Bit duration
Nsamples = int(Td*Fs) # Samples in one bit duration
Nsym = int(np.floor(np.size(t)/Nsamples))
# Python code to generate binary stream of data
sig = binary(Nsym, Nsamples)
# ASK waveform generation
Xask = x * -sig

# Xask = np.fft.fft(x)

figure, axis = plt.subplots(2)
axis[0].plot(t,x)
axis[0].set_title("Binary digital data")
axis[1].plot(t, Xask)
plt.yscale('log')
axis[1].set_title("ASK modulated signal")
plt.tight_layout()

plt.savefig("myImagePDF.pdf", format="pdf", bbox_inches="tight")

plt.show()