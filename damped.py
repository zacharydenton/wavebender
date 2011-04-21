#!/usr/bin/env python
from wavegen import *
from itertools import *

def ncycles(iterable, n):
    "Returns the sequence elements n times"
    return chain.from_iterable(repeat(tuple(iterable), n))

def waves():
    l = int(44100*0.4) # each note lasts 0.4 seconds
    
    # ACG ACG ACG ACG DCD DCD DCD DCD ...
    return cycle(chain(ncycles(chain(islice(damped_wave(frequency=440.0, amplitude=0.1, length=int(l/4)), l),
                                     islice(damped_wave(frequency=261.63, amplitude=0.1, length=int(l/4)), l),
                                     islice(damped_wave(frequency=329.63, amplitude=0.1, length=int(l/4)), l)), 4),
                 
                       ncycles(chain(islice(damped_wave(frequency=293.66, amplitude=0.1, length=int(l/4)), l),
                                     islice(damped_wave(frequency=261.63, amplitude=0.1, length=int(l/4)), l),
                                     islice(damped_wave(frequency=293.66, amplitude=0.1, length=int(l/4)), l)), 4)))

channels = ((waves(),), (waves(), white_noise(amplitude=0.01),))

samples = compute_samples(channels, 44100 * 60 * 1)
write_wavefile('damped.wav', samples)
