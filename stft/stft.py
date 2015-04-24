"""
Module to transform signals

"""
from __future__ import division
import scipy
import numpy
import math
import itertools
import scipy.interpolate
import scipy.fftpack
from .types import SpectrogramArray


def process(
    data,
    window,
    halved,
    transform,
    padding,
):
    """Calculate a windowed transform of a signal

    Parameters
    ----------
    data : array_like
        The signal to be calculated. Must be a 1D array.
    window : array_like
        Tapering window
    halved : boolean
        Switch for turning on signal truncation. For real signals, the fourier
        transform of real signals returns a symmetrically mirrored spectrum.
        This additional data is not needed and can be removed.
    transform : callable
        The transform to be used.
    padding : int
        Zero-pad signal with x times the number of samples.

    Returns
    -------
    data : array_like
        The spectrum

    """

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
    halved,
    transform,
    padding,
):
    """Calculate the inverse short time fourier transform of a spectrum

    Parameters
    ----------
    data : array_like
        The spectrum to be calculated. Must be a 1D array.
    window : array_like
        Tapering window
    halved : boolean
        Switch for turning on signal truncation. For real output signals, the
        inverse fourier transform consumes a symmetrically mirrored spectrum.
        This additional data is not needed and can be removed. Setting this
        value to :code:`True` will automatically create a mirrored spectrum.
    transform : callable
        The transform to be used.
    padding : int
        Signal before FFT transform was padded with x zeros.


    Returns
    -------
    data : array_like
        The signal

    """
    if halved:
        data = numpy.lib.pad(data, (0, data.shape[0] - 2), 'reflect')
        start = data.shape[0] // 2 + 1
        data[start:] = data[start:].conjugate()

    output = transform(data)

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
    halved=True,
    transform=None,
    padding=0,
    save_settings=True,
):
    """Calculate the spectrogram of a signal

    Parameters
    ----------
    data : array_like
        The signal to be transformed. May be a 1D vector for single channel or
        a 2D matrix for multi channel data. In case of a mono signal, the data
        is must be a 1D vector of length :code:`samples`. In case of a multi
        channel signal, the data must be in the shape of :code:`samples x
        channels`.
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
    halved : boolean
        Switch for turning on signal truncation. For real signals, the fourier
        transform of real signals returns a symmetrically mirrored spectrum.
        This additional data is not needed and can be removed. Defaults to
        :code:`True`.
    transform : callable
        The transform to be used. Defaults to :code:`scipy.fftpack.fft`.
    padding : int
        Zero-pad signal with x times the number of samples.
    save_settings : boolean
        Save settings used here in attribute :code:`out.stft_settings` so that
        :func:`ispectrogram` can infer these settings without the developer
        having to pass them again.

    Returns
    -------
    data : array_like
        The spectrogram (or tensor of spectograms) In case of a mono signal,
        the data is formatted as :code:`bins x frames`. In case of a multi
        channel signal, the data is formatted as :code:`bins x frames x
        channels`.

    Notes
    -----
    The data will be padded to be a multiple of the desired FFT length.

    See Also
    --------
    stft.stft.process : The function used to transform the data

    """
    if overlap is None:
        overlap = 2

    if hopsize is None:
        hopsize = framelength // overlap

    if halved and numpy.any(numpy.iscomplex(data)):
        raise ValueError("You cannot treat a complex input signal as real "
                         "valued. Please set keyword argument halved=False.")

    data = numpy.squeeze(data)

    if transform is None:
        transform = scipy.fftpack.fft

    if not isinstance(transform, (list, tuple)):
        transform = [transform]

    transforms = itertools.cycle(transform)

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
        window_array = window(framelength)
    else:
        window_array = window

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
                window=window_array,
                halved=halved,
                transform=next(transforms),
                padding=padding,
            ) / (framelength // hopsize // 2)

            if(i == 0):
                output = numpy.zeros(
                    (sig.shape[0], len(values)), dtype=sig.dtype
                )

            output[:, j] = sig

        return output

    if data.ndim > 2:
        raise ValueError("spectrogram: Only 1D or 2D input data allowed")
    if data.ndim == 1:
        out = traf(data)
    elif data.ndim == 2:
        for i in range(data.shape[1]):
            tmp = traf(data[:, i])

            if i == 0:
                out = numpy.empty(
                    (tmp.shape + (data.shape[1],)), dtype=tmp.dtype
                )
            out[:, :, i] = tmp

    if save_settings:
        out = SpectrogramArray(
            out,
            stft_settings={
                'framelength': framelength,
                'hopsize': hopsize,
                'overlap': overlap,
                'centered': centered,
                'window': window,
                'halved': halved,
                'transform': transform,
                'padding': padding,
            }
        )

    return out


def ispectrogram(
    data,
    framelength=None,
    hopsize=None,
    overlap=None,
    centered=None,
    window=None,
    halved=None,
    transform=None,
    padding=None,
):
    """Calculate the inverse spectrogram of a signal

    Parameters
    ----------
    data : array_like
        The spectrogram to be inverted. May be a 2D matrix for single channel
        or a 3D tensor for multi channel data. In case of a mono signal, the
        data must be in the shape of :code:`bins x frames`. In case of a multi
        channel signal, the data must be in the shape of :code:`bins x frames x
        channels`.
    framelength : int
        The signal frame length. Defaults to infer from data.
    hopsize : int
        The signal frame hopsize. Defaults to infer from data. Setting this
        value will override :code:`overlap`.
    overlap : int
        The signal frame overlap coefficient. Value :code:`x` means
        :code:`1/x` overlap. Defaults to infer from data.
    centered : boolean
        Pad input signal so that the first and last window are centered around
        the beginning of the signal. Defaults to to infer from data.
    window : callable, array_like
        Window to be used for deringing. Can be :code:`False` to disable
        windowing. Defaults to to infer from data.
    halved : boolean
        Switch to reconstruct the other halve of the spectrum if the forward
        transform has been truncated. Defaults to to infer from data.
    transform : callable
        The transform to be used. Defaults to infer from data.
    padding : int
        Zero-pad signal with x times the number of samples. Defaults to infer
        from data.

    Returns
    -------
    data : array_like
        The signal (or matrix of signals). In case of a mono output signal, the
        data is formatted as a 1D vector of length :code:`samples`. In case of
        a multi channel output signal, the data is formatted as :code:`samples
        x channels`.

    Notes
    -----
    By default :func:`spectrogram` saves its transformation parameters in
    the output array. This data is used to infer the transform parameters
    here. Any aspect of the settings can be overridden by passing the according
    parameter to this function.

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
    try:
        if framelength is None:
            framelength = data.stft_settings['framelength']
        if hopsize is None:
            hopsize = data.stft_settings['hopsize']
        if overlap is None:
            overlap = data.stft_settings['overlap']
        if centered is None:
            centered = data.stft_settings['centered']
        if window is None:
            window = data.stft_settings['window']
        if halved is None:
            halved = data.stft_settings['halved']
        if padding is None:
            padding = data.stft_settings['padding']
    except AttributeError:
        pass
    except KeyError:
        raise ValueError(
            "stft_settings dict was incomplete, could not"
            "infer data from array"
        )

    if overlap is None:
        overlap = 2

    if hopsize is None:
        hopsize = framelength // overlap

    if window is None:
        window = cosine

    if callable(window):
        window_array = window(framelength)
    else:
        window_array = window

    if transform is None:
        transform = scipy.fftpack.ifft

    if not isinstance(transform, (list, tuple)):
        transform = [transform]

    transforms = itertools.cycle(transform)

    def traf(data):
        i = 0
        values = range(0, data.shape[1])
        for j in values:
            sig = iprocess(
                data[:, j],
                window=window_array,
                halved=halved,
                transform=next(transforms),
                padding=padding,
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
