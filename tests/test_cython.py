def test_cython():
    import numpy
    from project import cython

    N = 100
    f = numpy.arange(N * N, dtype=numpy.int).reshape((N, N))
    g = numpy.arange(81, dtype=numpy.int).reshape((9, 9))

    assert type(cython.convolve(f, g)) == numpy.ndarray
