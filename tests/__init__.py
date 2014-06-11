import stft
import numpy
import scipy.fftpack
import nose


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


@nose.tools.raises(NotImplementedError)
def test_multichannel():
    """
    Test for matrix input when it should be a vector

    """
    siglen = 2048
    nchan = 2
    framelen = 512

    a = numpy.random.random((siglen, nchan))
    stft.spectrogram(a, framelength=framelen)


@nose.tools.raises(NotImplementedError)
def test_vector_inverse():
    """
    Test for any dimensions that are not a matrix

    """
    siglen = 2048
    framelen = 512

    a = numpy.random.random(siglen)
    stft.ispectrogram(a, framelength=framelen)
