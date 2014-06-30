"""
Module to transform signals

"""
from __future__ import division
import scipy
import numpy
import math
import scipy.interpolate


def process(data, window=None, halved=True, transform=None, padding=0, **kwargs):
    """
    Calculate a windowed transform of a signal

    Parameters
    ----------
    data : numpy array
        The signal to be calculated.
    window : callable
        Window to be used for deringing. Can be False to disable windowing.
        Defaults to `scipy.signal.cosine`.
    halved : boolean
        Switch for turning on signal truncation. By default,
        the fourier transform of real signals returns a symmetrically mirrored
        spectrum. This additional data is not needed and can be
        removed. Defaults to True.
    transform : callable
        The transform to be used. Defaults to `scipy.fft.
    padding : int
        Zero-pad signal with x times the number of samples.

    Returns
    -------
    data : numpy array
        The spectrum

    Notes
    -----

    Additional keyword arguments will be passed on to `transform`.

    """
    if transform is None:
        transform = scipy.fft

    if window is None:
        window = cosine

    if callable(window):
        data = data * window(len(data))

    if padding > 0:
        data = numpy.hstack((data, numpy.zeros(len(data) * padding)))

    result = transform(data)

    if(halved):
        result = result[0:result.size // 2 + 1]

    return result


def iprocess(data, window=None, halved=True, transform=None, padding=0, **kwargs):
    """
    Calculate the inverse short time fourier transform of a spectrum

    Parameters
    ----------
    data : numpy array
        The spectrum to be calculated.
    window : callable
        Window to be used for deringing. Can be False to disable windowing.
        Defaults to `scipy.signal.cosine`.
    halved : boolean
        Switch for turning on signal truncation. For real output signals,
        the inverse fourier transform consumes a symmetrically
        mirrored spectrum. This additional data is not needed
        and can be removed. Setting this value to True will
        automatically create a mirrored spectrum. Defaults to True.
    transform : callable
        The transform to be used. Defaults to `scipy.ifft`.
    padding : int
        Signal before FFT transform was padded with x zeros.

    Returns
    -------
    data : numpy array
        The signal

    Notes
    -----

    Additional keyword arguments will be passed on to `transform`.

    """
    if transform is None:
        transform = scipy.ifft

    if halved:
        data = numpy.hstack((data, data[-2:0:-1].conjugate()))

    output = transform(data, **kwargs)

    if padding > 0:
        output = output[0:-(len(data) * padding / (padding + 1))]

    if window is None:
        window = cosine

    if callable(window):
        output = output * window(len(output))

    return scipy.real(output)


def spectrogram(data, framelength=1024, hopsize=None, overlap=None, **kwargs):
    """
    Calculate the spectrogram of a signal

    Parameters
    ----------
    data : numpy array
        The signal to be transformed. May be a 1D vector for single channel
        or a 2D matrix for multi channel data.
    framelength : int
        The signal frame length. Defaults to 1024.
    hopsize : int
        The signal frame hopsize. Defaults to None. Setting this
        value will override `overlap`.
    overlap : int
        The signal frame overlap coefficient. Value x means
        1/x overlap. Defaults to 2.

    Returns
    -------
    data : numpy array
        The spectrogram (or tensor of spectograms)

    Notes
    -----

    Additional keyword arguments will be passed on to `process`.

    """
    if overlap is None:
        overlap = 2

    if hopsize is None:
        hopsize = framelength // overlap

    def traf(data):
        # Pad input signal so it fits into framelength spec
        data = numpy.hstack(
            (
                data,
                numpy.zeros(
                    math.ceil(len(data) / framelength) * framelength - len(data)
                )
            )
        )

        values = list(enumerate(
            range(0, len(data) - framelength + hopsize, hopsize)
        ))

        for j, i in values:
            sig = process(data[i:i + framelength], **kwargs) / (framelength // hopsize // 2)

            if(i == 0):
                output = numpy.zeros((sig.shape[0], len(values)), dtype=sig.dtype)

            output[:, j] = sig

        return output

    if data.ndim == 1:
        return traf(data)
    elif data.ndim == 2:
        for i in range(data.shape[1]):
            tmp = traf(data[:, i])

            if i == 0:
                out = numpy.empty((tmp.shape + (data.shape[1],)), dtype=tmp.dtype)
            out[:, :, i] = tmp
        return out
    else:
        raise ValueError("spectrogram: Only 1D or 2D input data allowed")


def ispectrogram(data, framelength=1024, hopsize=None, overlap=None, **kwargs):
    """
    Calculate the inverse spectrogram of a signal

    Parameters
    ----------
    data : numpy array
        The spectrogram to be inverted. May be a 2D matrix for single channel
        or a 3D tensor for multi channel data.
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
        The signal (or matrix of signals)

    Notes
    -----

    Additional keyword arguments will be passed on to `iprocess`.

    """
    if overlap is None:
        overlap = 2

    if hopsize is None:
        hopsize = framelength // overlap

    def traf(data):
        i = 0
        values = range(0, data.shape[1])
        for j in values:
            sig = iprocess(data[:, j], **kwargs)

            if(i == 0):
                output = numpy.zeros(
                    framelength + (len(values) - 1) * hopsize,
                    dtype=sig.dtype
                )

            output[i:i + framelength] += sig

            i += hopsize

        return output

    if data.ndim == 2:
        return traf(data)
    elif data.ndim == 3:
        for i in range(data.shape[2]):
            tmp = traf(data[:, :, i])

            if i == 0:
                out = numpy.empty((tmp.shape + (data.shape[2],)), dtype=tmp.dtype)
            out[:, i] = tmp
        return out
    else:
        raise ValueError("ispectrogram: Only 2D or 3D input data allowed")


def cosine(M):
    """
    Gernerate a halfcosine window of given length

    Uses `scipy.signal.cosine` by default. However since this window
    function has only recently been merged into mainline SciPy, a fallback
    calculation is in place.

    Parameters
    ----------
    M : int
        Length of the window.

    Returns
    -------
    data : numpy array
        The window function

    """
    try:
        import scipy.signal
        return scipy.signal.cosine(M)
    except AttributeError:
        return numpy.sin(numpy.pi / M * (numpy.arange(0, M) + .5))
