#!/usr/bin/env python
import wave
import math
import struct
import random
import argparse
from itertools import *

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def sine_wave(frequency=440.0, framerate=44100, amplitude=0.5):
    '''
    Generate a sine wave at a given frequency of infinite length.
    '''
    if amplitude > 1.0: amplitude = 1.0
    if amplitude < 0.0: amplitude = 0.0
    return (float(amplitude) * math.sin(2.0*math.pi*float(frequency)*(float(i)/float(framerate))) \
            for i in count(0))

def white_noise(amplitude=0.5):
    '''
    Generate random samples.
    '''
    return (float(amplitude) * (2 * random.random() - 1) for i in count(0))

def write_wavefile(filename, samples, nchannels, sampwidth, framerate):
    "Write samples to a wavefile."
    w = wave.open(filename, 'w')
    w.setparams((nchannels, sampwidth, framerate, 0, 'NONE', 'not compressed'))

    # split the samples into chunks, 1 second each (to reduce memory consumption)
    for chunk in grouper(framerate, samples):
        frames = ''.join(''.join(struct.pack('h', sample) for sample in channels) for channels in chunk)
        w.writeframes(frames)

    w.close()

    return filename

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--channels', help="Number of channels to produce", default=2, type=int)
    parser.add_argument('-b', '--bits', help="Number of bits in each sample", choices=(16,), default=16, type=int)
    parser.add_argument('-r', '--rate', help="Sample rate in Hz", default=44100, type=int)
    parser.add_argument('-d', '--duration', help="Duration of the wave in seconds.", default=60, type=int)
    parser.add_argument('-a', '--amplitude', help="Amplitude of the wave on a scale of 0.0-1.0.", default=0.5, type=float)
    parser.add_argument('-f', '--frequency', help="Frequency of the wave in Hz", default=440.0, type=float)
    parser.add_argument('filename', help="The file to generate.")
    args = parser.parse_args()

    max_amplitude = int((2 ** args.bits) / 2) - 1

    # create a sine wave in every channel and zip the waves together
    samples = izip(*(islice(imap(lambda s: int(float(max_amplitude) * s), \
                                 sine_wave(args.frequency, args.rate, args.amplitude)), \
                            args.duration * args.rate) \
                     for i in range(args.channels)))

    # add some white noise
    samples = ([(int(float(max_amplitude) * noise) + sample) for sample in channels] \
               for channels, noise in izip(samples, white_noise(0.1)))

    # write the samples to a file
    write_wavefile(args.filename, samples, args.channels, args.bits / 8, args.rate)

if __name__ == "__main__":
    main()
