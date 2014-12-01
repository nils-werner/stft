"""
Module to transform signals

"""
from __future__ import division
import scipy
import numpy
import math
import scipy.interpolate


def process(
    data,
    window,
    halved=True,
    transform=None,
    padding=0,
    **kwargs
):
    """Calculate a windowed transform of a signal

    Parameters
    ----------
    data : array_like
        The signal to be calculated.
    window : array_like
        Tapering window
    halved : boolean
        Switch for turning on signal truncation. By default,
        the fourier transform of real signals returns a symmetrically mirrored
        spectrum. This additional data is not needed and can be
        removed. Defaults to :code:`True`.
    transform : callable
        The transform to be used. Defaults to :code:`scipy.fft`.
    padding : int
        Zero-pad signal with x times the number of samples.

    Returns
    -------
    data : array_like
        The spectrum

    Notes
    -----
    Additional keyword arguments will be passed on to :code:`transform`.

    """
    if transform is None:
        transform = scipy.fft

    data = data * window

    if padding > 0:
        data = numpy.lib.pad(
            data,
            pad_width=(
                0,
                len(data) * padding
            ),
            mode='constant',
            constant_values=0
        )

    result = transform(data)

    if(halved):
        result = result[0:result.size // 2 + 1]

    return result


def iprocess(
    data,
    window,
    halved=True,
    transform=None,
    padding=0,
    **kwargs
):
    """Calculate the inverse short time fourier transform of a spectrum

    Parameters
    ----------
    data : array_like
        The spectrum to be calculated.
    window : array_like
        Tapering window
    halved : boolean
        Switch for turning on signal truncation. For real output signals,
        the inverse fourier transform consumes a symmetrically
        mirrored spectrum. This additional data is not needed
        and can be removed. Setting this value to :code:`True` will
        automatically create a mirrored spectrum. Defaults to :code:`True`.
    transform : callable
        The transform to be used. Defaults to :code:`scipy.ifft`.
    padding : int
        Signal before FFT transform was padded with x zeros.

    Returns
    -------
    data : array_like
        The signal

    Notes
    -----
    Additional keyword arguments will be passed on to :code:`transform`.

    """
    if transform is None:
        transform = scipy.ifft

    if halved:
        data = numpy.hstack((data, data[-2:0:-1].conjugate()))

    output = transform(data, **kwargs)

    if padding > 0:
        output = output[0:-(len(data) * padding / (padding + 1))]

    return scipy.real(output * window)


def spectrogram(
    data,
    framelength=1024,
    hopsize=None,
    overlap=None,
    centered=True,
    window=None,
    **kwargs
):
    """Calculate the spectrogram of a signal

    Parameters
    ----------
    data : array_like
        The signal to be transformed. May be a 1D vector for single channel
        or a 2D matrix for multi channel data.
        In case of a mono signal, the data is must be a 1D vector of length
        :code:`samples`.
        In case of a multi channel signal, the data must be in the shape of
        :code:`samples x channels`.
    framelength : int
        The signal frame length. Defaults to :code:`1024`.
    hopsize : int
        The signal frame hopsize. Defaults to :code:`None`. Setting this
        value will override :code:`overlap`.
    overlap : int
        The signal frame overlap coefficient. Value :code:`x` means
        :code:`1/x` overlap. Defaults to :code:`2`.
    centered : boolean
        Pad input signal so that the first and last window are centered around
        the beginning of the signal. Defaults to true.
    window : callable, array_like
        Window to be used for deringing. Can be :code:`False` to disable
        windowing. Defaults to :code:`scipy.signal.cosine`.

    Returns
    -------
    data : array_like
        The spectrogram (or tensor of spectograms)
        In case of a mono signal, the data is formatted as
        :code:`bins x frames`.
        In case of a multi channel signal, the data is formatted as
        :code:`bins x frames x channels`.

    Notes
    -----
    Additional keyword arguments will be passed on to :code:`process`.

    The data will be padded to be a multiple of the desired FFT length.

    See Also
    --------
    stft.stft.process : The function used to transform the data

    """
    if overlap is None:
        overlap = 2

    if hopsize is None:
        hopsize = framelength // overlap

    data = numpy.squeeze(data)

    if centered:
        padtuple = [(0, 0)] * data.ndim
        padtuple[0] = (framelength // 2, framelength // 2)
        data = numpy.lib.pad(
            data,
            pad_width=padtuple,
            mode='constant',
            constant_values=0
        )

    if window is None:
        window = cosine

    if callable(window):
        window = window(framelength)

    def traf(data):
        # Pad input signal so it fits into framelength spec
        data = numpy.lib.pad(
            data,
            pad_width=(
                0,
                int(
                    math.ceil(
                        len(data) / framelength
                    ) * framelength - len(data)
                )
            ),
            mode='constant',
            constant_values=0
        )

        values = list(enumerate(
            range(0, len(data) - framelength + hopsize, hopsize)
        ))

        for j, i in values:
            sig = process(
                data[i:i + framelength],
                window,
                **kwargs
            ) / (framelength // hopsize // 2)

            if(i == 0):
                output = numpy.zeros(
                    (sig.shape[0], len(values)), dtype=sig.dtype
                )

            output[:, j] = sig

        return output

    if data.ndim == 1:
        return traf(data)
    elif data.ndim == 2:
        for i in range(data.shape[1]):
            tmp = traf(data[:, i])

            if i == 0:
                out = numpy.empty(
                    (tmp.shape + (data.shape[1],)), dtype=tmp.dtype
                )
            out[:, :, i] = tmp
        return out
    else:
        raise ValueError("spectrogram: Only 1D or 2D input data allowed")


def ispectrogram(
    data,
    framelength=1024,
    hopsize=None,
    overlap=None,
    centered=True,
    window=None,
    **kwargs
):
    """Calculate the inverse spectrogram of a signal

    Parameters
    ----------
    data : array_like
        The spectrogram to be inverted. May be a 2D matrix for single channel
        or a 3D tensor for multi channel data.
        In case of a mono signal, the data must be in the shape of
        :code:`bins x frames`.
        In case of a multi channel signal, the data must be in the shape of
        :code:`bins x frames x channels`.
    framelength : int
        The signal frame length. Defaults to :code:`1024`.
    hopsize : int
        The signal frame hopsize. Defaults to :code:`None`. Setting this
        value will override :code:`overlap`.
    overlap : int
        The signal frame overlap coefficient. Value :code:`x` means
        :code:`1/x` overlap. Defaults to :code:`2`.
    centered : boolean
        Pad input signal so that the first and last window are centered around
        the beginning of the signal. Defaults to :code:`True`.
    window : callable, array_like
        Window to be used for deringing. Can be :code:`False` to disable
        windowing. Defaults to :code:`scipy.signal.cosine`.
    halved : boolean
        Switch for turning on signal truncation. By default,
        the fourier transform returns a symmetrically mirrored
        spectrum. This additional data is not needed and can be
        removed. Defaults to :code:`True`.

    Returns
    -------
    data : array_like
        The signal (or matrix of signals).
        In case of a mono output signal, the data is formatted as a 1D vector
        of length :code:`samples`.
        In case of a multi channel output signal, the data is formatted as
        :code:`samples x channels`.

    Notes
    -----
    Additional keyword arguments will be passed on to :code:`iprocess`.

    During transform the data will be padded to be a multiple of the desired
    FFT length. Hence, the result of the inverse transform might be longer
    than the input signal. However it is safe to remove the additional data,
    e.g. by using

    .. code:: python

        output.resize(input.shape)

    where :code:`input` is the input of :code:`stft.spectrogram()` and
    :code:`output` is the output of :code:`stft.ispectrogram()`

    See Also
    --------
    stft.stft.iprocess : The function used to transform the data

    """
    if overlap is None:
        overlap = 2

    if hopsize is None:
        hopsize = framelength // overlap

    if window is None:
        window = cosine

    if callable(window):
        window = window(framelength)

    def traf(data):
        i = 0
        values = range(0, data.shape[1])
        for j in values:
            sig = iprocess(
                data[:, j],
                window,
                **kwargs
            )

            if(i == 0):
                output = numpy.zeros(
                    framelength + (len(values) - 1) * hopsize,
                    dtype=sig.dtype
                )

            output[i:i + framelength] += sig

            i += hopsize

        return output

    if data.ndim == 2:
        out = traf(data)
    elif data.ndim == 3:
        for i in range(data.shape[2]):
            tmp = traf(data[:, :, i])

            if i == 0:
                out = numpy.empty(
                    (tmp.shape + (data.shape[2],)), dtype=tmp.dtype
                )
            out[:, i] = tmp
    else:
        raise ValueError("ispectrogram: Only 2D or 3D input data allowed")

    if centered:
        slicetuple = [slice(None)] * out.ndim
        slicetuple[0] = slice(framelength // 2, -framelength // 2)
        return out[slicetuple]
    else:
        return out


def cosine(M):
    """Gernerate a halfcosine window of given length

    Uses :code:`scipy.signal.cosine` by default. However since this window
    function has only recently been merged into mainline SciPy, a fallback
    calculation is in place.

    Parameters
    ----------
    M : int
        Length of the window.

    Returns
    -------
    data : array_like
        The window function

    """
    try:
        import scipy.signal
        return scipy.signal.cosine(M)
    except AttributeError:
        return numpy.sin(numpy.pi / M * (numpy.arange(0, M) + .5))
