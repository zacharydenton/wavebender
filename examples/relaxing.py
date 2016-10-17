#!/usr/bin/env python
from wavebender import *
from itertools import *

def ncycles(iterable, n):
    "Returns the sequence elements n times"
    return chain.from_iterable(repeat(tuple(iterable), n))

noise = cycle(islice(white_noise(amplitude=0.006), 44100))

l = 16
tl = int(44100*l*0.2)
pl = int(44100*l*0.3)
sl = int(44100*l*0.3)
length = 2*tl+pl+sl

up = list(islice(damped_wave(115.5, amplitude=0.4, length=tl),tl))
pause = islice(sine_wave(115.5, amplitude=0.4),pl)
down = reversed(up)
silence = islice(repeat(0),pl)

channels = (
            (cycle(chain(down,pause,up,silence)), noise),
            (cycle(chain(down,pause,up,silence)), noise),
            )

samples = compute_samples(channels)
write_pcm(stdout, samples)
