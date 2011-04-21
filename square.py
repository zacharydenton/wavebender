#!/usr/bin/env python
from wavegen import *
from math import cos

def strange_wave(frequency, amplitude=0.5):
    for sine, noise in izip(sine_wave(frequency, amplitude=1.0), white_noise(amplitude=0.1)):
        if noise == 0: continue
        yield amplitude * cos((sine**2 - noise) / noise)

#channels = ((square_wave(440.0, amplitude=0.1), strange_wave(1000.0, amplitude=0.1)),)
channels = ((strange_wave(1000.0, amplitude=0.1),),)

samples = compute_samples(channels, 44100 * 60 * 1)
write_wavefile('square.wav', samples, nchannels=1, 44100 * 60 * 1)
