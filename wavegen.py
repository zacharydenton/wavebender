#!/usr/bin/env python
import wave
import math
import struct
import argparse
from itertools import *

MAX_AMPLITUDE = 32767

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
    return (int(float(amplitude)*float(MAX_AMPLITUDE) * \
                math.sin(2.0*math.pi*float(frequency)*(float(i)/float(framerate)))) \
            for i in count(0))

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
    parser.add_argument('-b', '--bits', help="Number of bits in each sample", choices=(8, 16, 24), default=16, type=int)
    parser.add_argument('-r', '--rate', help="Sample rate in Hz", default=44100, type=int)
    parser.add_argument('-d', '--duration', help="Duration of the wave in seconds.", default=60, type=int)
    parser.add_argument('-a', '--amplitude', help="Amplitude of the wave on a scale of 0.0-1.0.", default=0.5, type=float)
    parser.add_argument('-f', '--frequency', help="Frequency of the wave in Hz", default=440.0, type=float)
    parser.add_argument('filename', help="The file to generate.")
    args = parser.parse_args()

    # create a sine wave in every channel and zip the waves together
    samples = izip(*(islice(sine_wave(args.frequency, args.rate, args.amplitude), args.duration * args.rate) \
                     for i in range(args.channels)))

    # write the samples to a file
    write_wavefile(args.filename, samples, args.channels, args.bits / 8, args.rate)

if __name__ == "__main__":
    main()
