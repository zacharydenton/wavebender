#!/usr/bin/env python
import re
from wavebender import *
from itertools import *

def sbagen_phrase(phrase):
    '''
    147.0+4.0/1.27 -> two sine_waves. one 145.0 hz; one 149.0 hz. each at amplitude of 0.0127.
    '''
    if 'pink' in phrase:
        amplitude = float(phrase.split('/')[-1]) / 100.0
        return (white_noise(amplitude),
                white_noise(amplitude))

    carrier, remainder = re.split('[+-]', phrase, 1)
    beatfreq, amplitude = remainder.split('/')

    carrier = float(carrier)
    beatfreq = float(beatfreq)
    amplitude = float(amplitude) / 100.0

    return (sine_wave((carrier - beatfreq/2), amplitude=amplitude),
            sine_wave((carrier + beatfreq/2), amplitude=amplitude))

def sbagen_line(line, length=None):
    '''
    Given a sequence of (l, r), (l, r), return a sequence of (l, l), (r, r).
    '''
    return izip(*(imap(lambda s: islice(s, length), sbagen_phrase(phrase)) for phrase in line.split()))

def sequencer(*seqs):
    '''
    (sine_wave(440), 44100 * 0.4), (sine_wave(261), 44100 * 0.4 * 3)
    '''
    return chain(*(islice(generator, duration) for generator, duration in seqs))

if sys.argv[1:]:
    channels = sbagen_line(' '.join(sys.argv[1:]))
else:
    sys.exit(1)

samples = compute_samples(channels)
write_wavefile(stdout, samples)
