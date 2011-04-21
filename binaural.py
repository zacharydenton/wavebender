#!/usr/bin/env python
from wavegen import *

channels = ((sine_wave(440.0, amplitude=0.1),),
            (sine_wave(445.0, amplitude=0.1),))

samples = compute_samples(channels, 44100 * 60 * 5)
write_wavefile('5hz.wav', samples)
