#!/usr/bin/env python
from wavebender import *
import sys

def violin(amplitude=0.1):
    # simulates a violin playing G.
    return (damped_wave(400.0, amplitude=0.76*amplitude, length=44100 * 5),
            damped_wave(800.0, amplitude=0.44*amplitude, length=44100 * 5),
            damped_wave(1200.0, amplitude=0.32*amplitude, length=44100 * 5),
            damped_wave(3400.0, amplitude=0.16*amplitude, length=44100 * 5),
            damped_wave(600.0, amplitude=1.0*amplitude, length=44100 * 5),
            damped_wave(1000.0, amplitude=0.44*amplitude, length=44100 * 5),
            damped_wave(1600.0, amplitude=0.32*amplitude, length=44100 * 5))

channels = (violin(),)
samples = compute_samples(channels, 44100 * 60 * 1)
write_wavefile(sys.stdout, samples, 44100 * 60 * 1, nchannels=1)
