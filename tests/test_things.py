import stft
import numpy
import pytest
import scipy.fftpack


@pytest.fixture(params=[1, 2])
def channels(request):
    return request.param


@pytest.fixture(params=[0, 1, 4])
def padding(request):
    return request.param


@pytest.fixture(params=[2048])
def length(request):
    return request.param


@pytest.fixture
def signal(channels, length):
    return numpy.squeeze(numpy.random.random((length, channels)))


@pytest.fixture(params=[512])
def framelength(request):
    return request.param


def test_windowlength_errors():
    """
    Test if way too short signals can be transformed

    """
    siglen = 512
    framelen = 2048

    stft.spectrogram(numpy.random.random(siglen), framelength=framelen)


def test_precision(channels, padding, signal, framelength):
    """
    Test if transform-inverse identity holds

    """
    a = signal

    x = stft.spectrogram(a, framelength=framelength, padding=padding)
    y = stft.ispectrogram(x, framelength=framelength, padding=padding)

    # Crop first and last frame
    assert numpy.allclose(
        a[framelength:-framelength], y[framelength:-framelength]
    )


def test_rms(channels, padding, signal, framelength):
    """
    Test if transform-inverse identity holds

    """
    a = signal

    x = stft.spectrogram(a, framelength=framelength, padding=padding)
    y = stft.ispectrogram(x, framelength=framelength, padding=padding)

    # Crop first and last frame
    assert numpy.sqrt(
        numpy.mean(
            (a[framelength:-framelength] - y[framelength:-framelength]) ** 2
        )
    ) < 1e-7


def test_maxdim():
    a = numpy.random.random((512, 2, 2))

    with pytest.raises(ValueError):
        stft.spectrogram(a)

    b = numpy.random.random((512, 2, 2, 3))
    with pytest.raises(ValueError):
        stft.ispectrogram(b)


def test_issue1():
    a = numpy.random.random((512, 1))

    b = stft.spectrogram(a)

    assert b.ndim == 2


def test_fallback():
    try:
        import scipy.signal
        del scipy.signal.cosine
        return test_windowlength_errors()
    except AttributeError:
        pass
