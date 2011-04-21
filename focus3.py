#!/usr/bin/env python
'''
Wave I - Discovery
------------------

Tape 1 - Orientation (Focus 3)
Hemisync, Energy Conversion Box, Gateway Affirmation, Resonant Tuning

l/r 300/304 plus 100 Hz and 500 Hz carriers without recognizeable Delta

+++ 100+0/10 302+4/10 500+0/10
'''
from wavegen import *
import sys

channels = ((sine_wave(300.0, amplitude=0.1), sine_wave(100.0, amplitude=0.1), sine_wave(500.0, amplitude=0.1)),
            (sine_wave(304.0, amplitude=0.1), sine_wave(100.0, amplitude=0.1), sine_wave(500.0, amplitude=0.1)))

samples = compute_samples(channels)
write_wavefile(sys.stdout, samples)
