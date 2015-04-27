import pytest
from stft.utils import pad, unpad


def test_padding(signal, framelength):
    if signal.ndim == 2:
        pytest.skip("not testing 3D data here")

    tmp = pad(signal, framelength)
    out = unpad(tmp, len(signal))

    assert out.shape == signal.shape
