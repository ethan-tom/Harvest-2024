import matplotlib.pyplot as plt
import numpy as np
def binary(sym, sym_len):

  import numpy as np
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
from math import pi
plt.close('all')
# Carrier wave and binary waveform configuration parameters
Fs = 1000 # Samples per second
fc = 25 # Carrier frequency 100 Hz, 100 cycles/sec
T = 1 # Total simulation time in seconds
t = np.arange(0, T, 1/Fs)
x =np.sin(2*pi*fc*t)
Td = 0.1 # Bit duration
Nsamples = int(Td*Fs) # Samples in one bit duration
Nsym = int(np.floor(np.size(t)/Nsamples))
# Python code to generate binary stream of data
sig = binary(Nsym, Nsamples)
# ASK waveform generation
xx = []
for z in t:
    xx.append(z*np.random.randint(-100, 100)*1e-6)
Xask = x * sig
# Binary waveform and ASK waveform Plots
figure, axis = plt.subplots(2)
axis[0].plot(t,sig)
axis[0].set_title("Binary digital data")
axis[1].plot(t, Xask)
axis[1].set_title("ASK modulated signal")
plt.tight_layout()
plt.show()