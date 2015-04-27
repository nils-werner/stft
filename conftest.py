from __future__ import division
import numpy
import pytest
import stft


@pytest.fixture(params=[1, 2, 4])
def channels(request):
    return request.param


@pytest.fixture(params=[0, 1, 4])
def padding(request):
    return request.param


@pytest.fixture(params=[2, 4, 5])
def length(request):
    return request.param * 1024


@pytest.fixture(params=[stft.stft.cosine, 1])
def window(request):
    return request.param


@pytest.fixture
def signal(channels, length):
    return numpy.squeeze(numpy.random.random((length, channels)))


@pytest.fixture(params=[1, 2, 4])
def framelength(request):
    return request.param * 512


@pytest.fixture(params=[True, False])
def halved(request):
    return request.param
