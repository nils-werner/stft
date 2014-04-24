"""
Module to transform signals

"""
from . import window
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
        data = window.window(data)

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
        output = window.window(output)

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
