#!/usr/bin/env python
'''
Installer script for the wavebender module.
'''

from distutils.core import setup
import wavebender

setup (
    name = "wavebender",
    description = "An audio synthesis library for Python.",

    author = wavebender.__author__,
    author_email = wavebender.__author_email__,
    version = wavebender.__version__,
    url = wavebender.__url__,
    long_description = wavebender.__longdescr__,
    classifiers = wavebender.__classifiers__,
    packages = ['wavebender',],
)
