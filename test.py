#!/usr/bin/env python

import soundfile as sf
import math
import numpy as np
import pylab

samples, sample_rate = sf.read("/home/gkorovkin/dtmf_tones.wav")

window_time = 20 #ms
window_samples_count = window_time * sample_rate / 1000
window_count = len(samples) / window_samples_count

print "Window samples count : ", window_samples_count, window_count



def goertzel_mag( samples, sample_rate, freq ):

    numsamples = float(len(samples))
    scaling_factor = 1.0 #numsamples / 2.0
    k = 0.5 + numsamples * freq / sample_rate
    omega = ( 2.0 * math.pi * k ) / numsamples
    sine = math.sin( omega )
    cosine = math.cos( omega )
    coeff = 2.0 * cosine
    q0 = 0.0
    q1 = 0.0
    q2 = 0.0

    for n in samples:
	q0 = coeff * q1 - q2 + n
	q2 = q1
	q1 = q0

    real = (q1 - q2 * cosine) / scaling_factor
    imag = (q2 * sine ) / scaling_factor

    mag = real**2 + imag**2

    #set to 0 if no threshold
    if mag < 4.0e-5:
	mag = 0
    return math.sqrt( mag )


def goertzel(samples, sample_rate, *freqs):
    """
    Implementation of the Goertzel algorithm, useful for calculating individual
    terms of a discrete Fourier transform.
    `samples` is a windowed one-dimensional signal originally sampled at `sample_rate`.
    The function returns 2 arrays, one containing the actual frequencies calculated,
    the second the coefficients `(real part, imag part, power)` for each of those frequencies.
    For simple spectral analysis, the power is usually enough.
    Example of usage :

	freqs, results = goertzel(some_samples, 44100, (400, 500), (1000, 1100))
    """
    window_size = len(samples)
    f_step = sample_rate / float(window_size)
    f_step_normalized = 1.0 / window_size

    # Calculate all the DFT bins we have to compute to include frequencies
    # in `freqs`.
    bins = set()
    for f_range in freqs:
	f_start, f_end = f_range
	k_start = int(math.floor(f_start / f_step))
	k_end = int(math.ceil(f_end / f_step))

	if k_end > window_size - 1: raise ValueError('frequency out of range %s' % k_end)
	bins = bins.union(range(k_start, k_end))

    # For all the bins, calculate the DFT term
    n_range = range(0, window_size)
    freqs = []
    results = []
    for k in bins:

	# Bin frequency and coefficients for the computation
	f = k * f_step_normalized
	w_real = 2.0 * math.cos(2.0 * math.pi * f)
	w_imag = math.sin(2.0 * math.pi * f)

	# Doing the calculation on the whole sample
	d1, d2 = 0.0, 0.0
	for n in n_range:
	    y  = samples[n] + w_real * d1 - d2
	    d2, d1 = d1, y

	# Storing results `(real part, imag part, power)`
	results.append((
	    0.5 * w_real * d1 - d2, w_imag * d1,
	    d2**2 + d1**2 - w_real * d1 * d2)
	)
	freqs.append(f * sample_rate)
    return freqs, results


for w_idx in range(0, window_count ):
    offset = w_idx * window_samples_count

    # applying Goertzel on those signals, and plotting results
    sub_samples = samples[ offset : offset + window_samples_count ]
    dtmf_low_band = [ 697, 770, 852, 941, 1209, 1336, 1477, 1633 ]
    magn = []
    for freq in dtmf_low_band:
	magn.append( goertzel_mag(sub_samples, sample_rate,freq ) )

    pylab.subplot(2, 2, 1)
    pylab.title('(1) Sine wave 440Hz + 1020Hz')
    pylab.plot(range(0,len(sub_samples)), sub_samples)

    pylab.subplot(2, 2, 3)
    pylab.title('(1) Goertzel Algo, freqency magn')
    pylab.plot(dtmf_low_band, magn, 'o')
    #pylab.ylim([0,100000])
    pylab.show()
    #process_sub_samples(data[offset : offset + window_samples_count])
