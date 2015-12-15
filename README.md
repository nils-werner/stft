STFT
====

[![Build Status](https://travis-ci.org/audiolabs/stft.svg?branch=master)](https://travis-ci.org/audiolabs/stft)
[![Docs Status](https://readthedocs.org/projects/stft/badge/?version=latest)](https://stft.readthedocs.org/en/latest/)

This is a package for calculating the short time fourier transform (spectrogram) or any
other transform in a lapped and windowed fashion.

Installation
------------

You can install this library using `pip`:

    pip install stft


Usage
-----

Loading a file and calculating the spectrogram, its inverse and saving the
result.

    import stft
    import scipy.io.wavfile as wav

    fs, audio = wav.read('input.wav')
    specgram = stft.spectrogram(audio)
    output = stft.ispectrogram(specgram)
    wav.write('output.wav', fs, output)
