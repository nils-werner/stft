import stft
import numpy
import pytest
import scipy.fftpack


def test_windowlength_errors():
    """
    Test if way too short signals can be transformed

    """
    siglen = 512
    framelen = 2048

    stft.spectrogram(numpy.random.random(siglen), framelength=framelen)


def test_precision():
    """
    Test if transform-inverse identity holds

    """
    for channels in [1, 2]:
        for padding in [0, 1, 4]:
            siglen = 2048
            framelen = 512

            a = numpy.squeeze(numpy.random.random((siglen, channels)))
            x = stft.spectrogram(a, framelength=framelen, padding=padding)
            y = stft.ispectrogram(x, framelength=framelen, padding=padding)

            # Crop first and last frame
            assert numpy.allclose(a[framelen:-framelen], y[framelen:-framelen])


def test_maxdim():
    a = numpy.random.random((512, 2, 2))

    with pytest.raises(ValueError):
        stft.spectrogram(a)

    b = numpy.random.random((512, 2, 2, 3))
    with pytest.raises(ValueError):
        stft.ispectrogram(b)


def test_fallback():
    try:
        import scipy.signal
        del scipy.signal.cosine
        return test_windowlength_errors()
    except AttributeError:
        pass
