#!/usr/bin/env python
"""
An audio synthesis library for Python.

It makes heavy use of the `itertools` module.
Good luck! (This is a work in progress.)
"""
import sys
import math
from . import wave
import struct
import random
import argparse
from itertools import count, islice

try:
    from itertools import zip_longest
except ImportError:
    from itertools import imap as map
    from itertools import izip as zip
    from itertools import izip_longest as zip_longest

try:
    stdout = sys.stdout.buffer
except AttributeError:
    stdout = sys.stdout

# metadata
__author__ = 'Zach Denton'
__author_email__ = 'zacharydenton@gmail.com'
__version__ = '0.3'
__url__ = 'http://github.com/zacharydenton/wavebender'
__longdescr__ = '''
An audio synthesis library for Python.
'''
__classifiers__ = [
    'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis'
]

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

def sine_wave(frequency=440.0, framerate=44100, amplitude=0.5,
        skip_frame=0):
    '''
    Generate a sine wave at a given frequency of infinite length.
    '''
    if amplitude > 1.0: amplitude = 1.0
    if amplitude < 0.0: amplitude = 0.0
    for i in count(skip_frame):
        sine = math.sin(2.0 * math.pi * float(frequency) * (float(i) / float(framerate)))
        yield float(amplitude) * sine

def square_wave(frequency=440.0, framerate=44100, amplitude=0.5):
    for s in sine_wave(frequency, framerate, amplitude):
        if s > 0:
            yield amplitude
        elif s < 0:
            yield -amplitude
        else:
            yield 0.0

def damped_wave(frequency=440.0, framerate=44100, amplitude=0.5, length=44100):
    if amplitude > 1.0: amplitude = 1.0
    if amplitude < 0.0: amplitude = 0.0
    return (math.exp(-(float(i%length)/float(framerate))) * s for i, s in enumerate(sine_wave(frequency, framerate, amplitude)))

def white_noise(amplitude=0.5):
    '''
    Generate random samples.
    '''
    return (float(amplitude) * random.uniform(-1, 1) for i in count(0))

def compute_samples(channels, nsamples=None):
    '''
    create a generator which computes the samples.

    essentially it creates a sequence of the sum of each function in the channel
    at each sample in the file for each channel.
    '''
    return islice(zip(*(map(sum, zip(*channel)) for channel in channels)), nsamples)

def write_wavefile(f, samples, nframes=None, nchannels=2, sampwidth=2, framerate=44100, bufsize=2048):
    "Write samples to a wavefile."
    if nframes is None:
        nframes = 0

    w = wave.open(f, 'wb')
    w.setparams((nchannels, sampwidth, framerate, nframes, 'NONE', 'not compressed'))

    max_amplitude = float(int((2 ** (sampwidth * 8)) / 2) - 1)

    # split the samples into chunks (to reduce memory consumption and improve performance)
    for chunk in grouper(bufsize, samples):
        frames = b''.join(b''.join(struct.pack('h', int(max_amplitude * sample)) for sample in channels) for channels in chunk if channels is not None)
        w.writeframesraw(frames)
    
    w.close()

def write_pcm(f, samples, sampwidth=2, framerate=44100, bufsize=2048):
    "Write samples as raw PCM data."
    max_amplitude = float(int((2 ** (sampwidth * 8)) / 2) - 1)

    # split the samples into chunks (to reduce memory consumption and improve performance)
    for chunk in grouper(bufsize, samples):
        frames = b''.join(b''.join(struct.pack('h', int(max_amplitude * sample)) for sample in channels) for channels in chunk if channels is not None)
        f.write(frames)

    f.close()

def main():
    parser = argparse.ArgumentParser(prog="wavebender")
    parser.add_argument('-c', '--channels', help="Number of channels to produce", default=2, type=int)
    parser.add_argument('-b', '--bits', help="Number of bits in each sample", choices=(16,), default=16, type=int)
    parser.add_argument('-r', '--rate', help="Sample rate in Hz", default=44100, type=int)
    parser.add_argument('-t', '--time', help="Duration of the wave in seconds.", default=60, type=int)
    parser.add_argument('-a', '--amplitude', help="Amplitude of the wave on a scale of 0.0-1.0.", default=0.5, type=float)
    parser.add_argument('-f', '--frequency', help="Frequency of the wave in Hz", default=440.0, type=float)
    parser.add_argument('filename', help="The file to generate.")
    args = parser.parse_args()

    # each channel is defined by infinite functions which are added to produce a sample.
    channels = ((sine_wave(args.frequency, args.rate, args.amplitude),) for i in range(args.channels))

    # convert the channel functions into waveforms
    samples = compute_samples(channels, args.rate * args.time)

    # write the samples to a file
    if args.filename == '-':
        filename = stdout
    else:
        filename = args.filename
    write_wavefile(filename, samples, args.rate * args.time, args.channels, args.bits // 8, args.rate)

if __name__ == "__main__":
    main()
