"""
Module to transform signals

"""
from .. import Window
from . import bins
from . import scale
from . import fractional
import scipy
import numpy
import math
import scipy.interpolate


def stft(data, windowed=True, halved=True, padding=0):
    """
    Calculate the short time fourier transform of a signal

    Parameters
    ----------
    data : numpy array
        The signal to be calculated.
    windowed : boolean
        Switch for turning on signal windowing. Defaults to True.
    halved : boolean
        Switch for turning on signal truncation. By default,
        the fourier transform returns a symmetrically mirrored
        spectrum. This additional data is not needed and can be
        removed. Defaults to True.
    padding : int
        Zero-pad signal with x times the number of samples.

    Returns
    -------
    data : numpy array
        The spectrum

    """
    if(windowed):
        data = Window.window(data)

    if(padding):
        data = numpy.hstack((data, numpy.zeros(len(data) * padding)))

    result = scipy.fft(data)

    if(halved):
        result = result[0:result.size / 2 + 1]

    return result


def istft(data, windowed=True, halved=True, padding=0):
    """
    Calculate the inverse short time fourier transform of a spectrum

    Parameters
    ----------
    data : numpy array
        The spectrum to be calculated.
    windowed : boolean
        Switch for turning on signal windowing. Defaults to True.
    halved : boolean
        Switch for turning on signal truncation. By default,
        the inverse fourier transform consumes a symmetrically
        mirrored spectrum. This additional data is not needed
        and can be removed. Defaults to True.
    padding : int
        Signal before FFT transform was padded with x zeros.

    Returns
    -------
    data : numpy array
        The signal

    """
    if(halved):
        data = numpy.hstack((data, data[-2:0:-1].conjugate()))

    output = scipy.ifft(data)

    if(padding):
        output = output[0:-(len(data) * padding / (padding + 1))]

    if(windowed):
        output = Window.window(output)

    return scipy.real(output)

fft = stft
ifft = istft


def spectrogram(data, framelength=1024, hopsize=None, overlap=None, transform=None, **kwargs):
    """
    Calculate the spectrogram of a signal

    Parameters
    ----------
    data : numpy array
        The signal to be calculated.
    framelength : int
        The signal frame length. Defaults to 1024.
    hopsize : int
        The signal frame hopsize. Defaults to None. Setting this
        value will override `overlap`.
    overlap : int
        The signal frame overlap coefficient. Value x means
        1/x overlap. Defaults to 2.
    windowed : boolean
        Switch for turning on signal windowing. Defaults to True.
    halved : boolean
        Switch for turning on signal truncation. By default,
        the fourier transform returns a symmetrically mirrored
        spectrum. This additional data is not needed and can be
        removed. Defaults to True.

    Returns
    -------
    data : numpy array
        The spectrogram

    """
    if transform is None:
        transform = stft

    if overlap is None:
        overlap = 2

    if hopsize is None:
        hopsize = framelength // overlap

    values = list(enumerate(
        range(0, len(data) - framelength, hopsize)
    ))
    for j, i in values:
        sig = transform(data[i:i + framelength], **kwargs) / (framelength // hopsize // 2)

        if(i == 0):
            output = numpy.zeros((len(values), sig.shape[0]), dtype=sig.dtype)

        output[j, :] = sig

    return output


def ispectrogram(data, framelength=1024, hopsize=None, overlap=None, transform=None, **kwargs):
    """
    Calculate the inverse spectrogram of a signal

    Parameters
    ----------
    data : numpy array
        The spectrogram to be calculated.
    framelength : int
        The signal frame length. Defaults to 1024.
    hopsize : int
        The signal frame hopsize. Defaults to None. Setting this
        value will override `overlap`.
    overlap : int
        The signal frame overlap coefficient. Value x means
        1/x overlap. Defaults to 2.
    windowed : boolean
        Switch for turning on signal windowing. Defaults to True.
    halved : boolean
        Switch for turning on signal truncation. By default,
        the fourier transform returns a symmetrically mirrored
        spectrum. This additional data is not needed and can be
        removed. Defaults to True.

    Returns
    -------
    data : numpy array
        The signal

    """
    if transform is None:
        transform = istft

    if overlap is None:
        overlap = 2

    if hopsize is None:
        hopsize = framelength // overlap

    i = 0
    values = range(0, data.shape[0])
    for j in values:
        sig = transform(data[j, :], **kwargs)

        if(i == 0):
            output = numpy.zeros(
                framelength + (len(values) - 1) * hopsize,
                dtype=sig.dtype
            )

        output[i:i + framelength] += sig

        i += hopsize

    return output


def constantQ(data, sf, bands=48, minf=50.0, oversampling=1, bwfactor=8.0):
    """
    Calculate the constant Q transform of a signal

    Parameters
    ----------
    data : numpy array
        The signal to be calculated.
    sf : int
        The sampling frequency
    bands : int
        Number of bands per octave. Defaults to 48.
    minf : float
        Minimum frequency to use. Defaults to 50Hz.
    oversampling : int
        Oversampling factor. Defaults to 1.
    bwfactor : float
        Bandwidth factor of bandpass filters. Defaults to 8.

    Returns
    -------
    data : numpy array
        A 2D matrix consisting of the transformed signal.

    """
    numBands = int(
        math.floor(math.log(sf / minf / 2.0) / math.log(2.0) * bands)
    )

    filterLength = numpy.zeros(numBands, dtype=int)
    bufferIndex = numpy.zeros(numBands, dtype=int)
    exp = numpy.zeros((numBands, 3), dtype=complex)
    pFactor = numpy.ones((numBands, 3), dtype=complex)
    out = numpy.zeros((numBands, 3), dtype=complex)

    relBandwidth = bwfactor * (2.0 ** (1.0 / bands) - 1.0)

    fCenter = minf * (2.0 ** (numpy.arange(0, numBands) / bands))
    bandwidth = fCenter * relBandwidth

    filterLength = numpy.floor(2.0 * sf / bandwidth).astype(int)

    exp[:, 0] = numpy.exp(-1j * 2.0 * numpy.pi * fCenter / sf)
    exp[:, 1] = numpy.exp(
        -1j * 2.0 * numpy.pi * (fCenter - bandwidth / 2.0) / sf
    )
    exp[:, 2] = numpy.exp(
        -1j * 2.0 * numpy.pi * (fCenter + bandwidth / 2.0) / sf
    )

    frameLength = int(
        math.floor(2.0 * sf / numpy.max(bandwidth) / float(oversampling))
    )

    buffer = numpy.zeros((numBands, numpy.max(filterLength), 3), dtype=complex)

    numFrames = data.shape[0] // frameLength
    plot = numpy.zeros((numFrames, numBands))

    allRows = numpy.arange(numBands)

    for frame in range(numFrames):
        for n in range(0, frameLength):
            x = data[frame * frameLength + n]

            xMod = x * pFactor
            out += xMod - buffer[allRows, bufferIndex, :]
            buffer[allRows, bufferIndex, :] = xMod

            pFactor *= exp
                # for long signals, these factors might have to be normalized
                # in order to avoid magnitudes deviating from 1 by numerical
                # inaccuracies

            bufferIndex += 1
            bufferIndex %= filterLength

        # the weighted sum of the phase corrected three outputs gives the final
        # output
        plot[frame, :] = numpy.abs(
            numpy.sum(
                (numpy.array([1.0, -0.5, -0.5]) * out[:, :]) *
                pFactor[:, :].conjugate(), axis=1
            )
        )

    return plot


def slidingwindow(data, size=11, stepsize=1, padded=True):
    """
    Calculate a sliding window over a signal

    Parameters
    ----------
    data : numpy array
        The spectrogram to be calculated.
    size : int
        The sliding window size
    padding : boolear
        Switch for turning on signal padding by mirroring
        on either side. Defaults to True.

    Returns
    -------
    data : numpy array
        A matrix where each line consists of one instance
        of the sliding window.

    Notes
    -----

    a = numpy.array([1, 2, 3, 4])
    slidingwindow(a, size=3)
    # >>> numpy.array([1, 1, 2],
    #                 [1, 2, 3],
    #                 [2, 3, 4],
    #                 [3, 4, 4])

    """
    if(size % 2 == 0):
        size += 1
    halfsize = numpy.floor(size / 2)
    if padded:
        tmp = numpy.hstack(
            (data[halfsize - 1::-1], data, data[:-halfsize - 1:-1])
        )
    else:
        tmp = data

    strides = (stepsize*tmp.itemsize, tmp.itemsize)
    shape = (1 + (tmp.nbytes - size * tmp.itemsize) / strides[0], size)

    return numpy.lib.stride_tricks.as_strided(
        tmp, shape=shape, strides=strides
    )
