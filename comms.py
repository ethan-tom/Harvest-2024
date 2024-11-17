import adi
import numpy as np

def parsein(indata, N, drone, inrate):
    Td = 0.01
    freq_table = list(N)
    for i in range(N):
      freq_table[i]=indata[i][drone.freq]
    time_table=list(N)
    for i in range(N):
       time_table = i*inrate
    
    
 
       

def receive(drone, station_sdr):
    sample_rate = 10000 # Hz
    center_freq = drone.freq # Hz
    num_samps = sample_rate*10*64*0.01 # number of samples returned per call to rx()

    sdr = adi.Pluto(station_sdr)
    sdr.gain_control_mode_chan0 = 'manual'
    sdr.rx_hardwaregain_chan0 = 70.0 # dB
    sdr.rx_lo = int(center_freq)
    sdr.sample_rate = int(sample_rate)
    sdr.rx_rf_bandwidth = int(sample_rate) # filter width, just set it to the same as sample rate for now
    sdr.rx_buffer_size = num_samps
    sdr.rx_enabled_channels = [0]

    samples = sdr.rx()
    return parsein(samples, num_samps, drone, sample_rate)

def binlist(data):
    string = bin(data)
    return [1 if string[x]=='1' else 0 for x in range(2, 66)]


def binary(sym, sym_len, data):
  rand_n = binlist(int(data))

  sig = np.zeros(int(sym*sym_len))

  # generating symbols
  id1 = np.where(rand_n == 1)

  for i in id1[0]:
    temp = int(i*sym_len)
    sig[temp:temp+sym_len] = 1
  return sig


def transmit(drone, data, command, station_sdr):
    sample_rate = 1e6 # Hz
    center_freq = drone.freq # Hz

    Fs = sample_rate # Samples per second
    fc = center_freq  # Carrier frequency 100 Hz, 100 cycles/sec
    Td = 0.01 # Bit duration
    T = Td*64 # Total simulation time in seconds
    t = np.arange(0, T, 1/Fs)
    x = np.sin(2*np.pi*fc*t)
    Nsamples = int(Td*Fs) # Samples in one bit duration
    Nsym = int(np.floor(np.size(t)/Nsamples))

    sdr = adi.Pluto(station_sdr)
    sdr.sample_rate = int(sample_rate)
    sdr.tx_rf_bandwidth = int(sample_rate) # filter cutoff, just set it to the same as sample rate
    sdr.tx_lo = int(center_freq)
    sdr.tx_hardwaregain_chan0 = 0 # Increase to increase tx power, valid range is -90 to 0 dB

    if type(data)==float:
       bull = 0b01
    elif type(data)==int:
       bull=0b00
    elif type(data)==None:
       bull = 0b10
    else:
       bull = 0b11 # bull- dtype bits, 01 = float, int  = 00, null = 10, unsupported = 11  
    sig = binary(Nsym, Nsamples, bitconstruct(command, drone.regnohash, bull, data, 0, 0b1))
    # ASK waveform generation
    Xask = x * sig
    samples = 2**14*Xask # The PlutoSDR expects samples to be between -2^14 and +2^14, not -1 and +1 like some SDRs
    for i in range(5):
        sdr.tx(samples) # transmit the batch of samples once

def bitconstruct(cmd, regno, dtype, data, parity, id):
   return(cmd<<58) | (regno<<42) | (dtype<<40) | (data<<8) | (parity<<1) | id

def turnOffK(n,k):
    # Do & of n with a number
    # with all set bits except
    # the k'th bit
   for j in range(k):
      n= (n & ~(1 << (j - 1)))
   return n


def reverse_bitconstruct(encoded_value): 
   cmd = encoded_value>>58
   regno = turnOffK(encoded_value>>42, 5)
   dtype = turnOffK(encoded_value>>40, 22)
   data = turnOffK(encoded_value>>8, 24)
   parity = turnOffK(encoded_value>>1, 56)
   id = turnOffK(encoded_value, 63)
   return cmd, regno, dtype, data, parity, id
