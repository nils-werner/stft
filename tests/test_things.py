from __future__ import division
import stft
import scipy
import numpy
import pytest


def test_shape(length, framelength):
    a = numpy.squeeze(numpy.random.random((length, 1)))

    x = stft.spectrogram(a, framelength=framelength, halved=True)
    assert x.shape[0] == framelength / 2 + 1

    x_2 = stft.spectrogram(a, framelength=framelength, halved=False)
    assert x_2.shape[0] == framelength


def test_window_types(signal, framelength, window):
    """
    Test if callable and fixed value windows work

    """
    stft.spectrogram(signal, framelength=framelength, window=window)


def test_windowlength_errors():
    """
    Test if way too short signals can be transformed

    """
    siglen = 512
    framelen = 2048

    stft.spectrogram(numpy.random.random(siglen), framelength=framelen)


def test_precision(channels, padding, signal, framelength, halved):
    """
    Test if transform-inverse identity holds

    """
    a = signal

    x = stft.spectrogram(
        a, framelength=framelength, padding=padding, halved=halved
    )
    y = stft.ispectrogram(x)

    assert numpy.allclose(a, y)


def test_overriding(channels, padding, signal, framelength):
    """
    Test if overriding transform settings works

    """
    a = signal

    x = stft.spectrogram(a, framelength=framelength, padding=padding)
    y = stft.ispectrogram(x, framelength=framelength)

    # We were using no overlap during inverse, so our output is twice as long
    assert numpy.allclose(a, y)


def test_multiple_transforms(signal):
    """
    Test if giving multiple different transforms works OK

    """
    a = signal

    x = stft.spectrogram(a, transform=[scipy.fftpack.fft, numpy.fft.fft])
    y = stft.ispectrogram(x, transform=[scipy.fftpack.ifft, numpy.fft.ifft])

    assert numpy.allclose(a, y)


def test_complex(signal):
    """
    Test transform-inverse works for complex input

    """
    a = signal

    # create complex test vectors by adding random phase
    c = a + 1j*numpy.random.random(a.shape)
    x = stft.spectrogram(c, halved=False)
    y = stft.ispectrogram(x, halved=False)

    assert c.dtype == y.dtype
    assert numpy.allclose(c, y)


def test_rms(channels, padding, signal, framelength, halved):
    """
    Test if transform-inverse identity holds

    """
    a = signal

    x = stft.spectrogram(
        a, framelength=framelength, padding=padding, halved=halved
    )
    y = stft.ispectrogram(x)

    assert numpy.sqrt(numpy.mean((a - y) ** 2)) < 1e-8


def test_maxdim():
    """
    Test if breaking elementary limitations (2D signal, 3D spectrogram at most)
    are caught appropriately

    """
    a = numpy.random.random((512, 2, 2))

    with pytest.raises(ValueError):
        stft.spectrogram(a)

    b = numpy.random.random((512, 2, 2, 3))
    with pytest.raises(ValueError):
        # we cannot infer data from a NumPy array, so we set framelengt here
        stft.ispectrogram(b, framelength=1024)


def test_issue1():
    """
    Passing a (x, 1) shape signal created a 3D tensor output, while
    a (x,) shape signal created a 2D matrix. This should not happen.

    """
    a = numpy.random.random((512, 1))

    b = stft.spectrogram(a)

    assert b.ndim == 2


def test_issue_autoinverse_values(signal, framelength):
    """
    Passing values to inverse on a plain array failed as the values were
    not actually used

    """
    x = numpy.array(stft.spectrogram(signal, framelength=framelength))
    y = stft.ispectrogram(x, framelength=framelength)


def test_issue_autoinverse_defaults(signal):
    """
    Using defaults in inverse did not work because there were none in place

    """
    x = numpy.array(stft.spectrogram(signal))
    y = stft.ispectrogram(x)


def raiser(*args):
    raise AttributeError


def test_fallback(monkeypatch):
    """
    Try monkeypatching signal.cosine away so we can test stft.stft.cosine.
    Ignore AttributeErrors during monkeypatching, for older scipy versions

    """
    import scipy.signal
    try:
        monkeypatch.setattr("scipy.signal.cosine", raiser)
    except Exception:
        pass
    return test_windowlength_errors()
