import stft
import numpy
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
    siglen = 2048
    framelen = 512

    a = numpy.random.random(siglen)
    x = stft.spectrogram(a, framelength=framelen)
    y = stft.ispectrogram(x, framelength=framelen)

    # Crop first and last frame
    assert numpy.allclose(a[framelen:-framelen], y[framelen:-framelen])
