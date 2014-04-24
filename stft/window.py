"""
Module to weigh a signal with a windowing function

"""
import numpy


def halfsin(M):
    """
    Gernerate a halfsin/halfcosine window of given length

    Uses `scipy.signal.cosine` by default. However since this window
    function has only recently been merged into mainline SciPy, a fallback
    calculation is in place.

    Parameters
    ----------
    M : int
        Length of the window.

    Returns
    -------
    data : numpy array
        The window function

    """
    try:
        import scipy.signal
        return scipy.signal.cosine(M)
    except AttributeError:
        return numpy.sin(numpy.pi / M * (numpy.arange(0, M) + .5))


def window(data):
    """
    Weigh a signal with the halfsin window function

    Parameters
    ----------
    data : numpy array
        The input signal.

    Returns
    -------
    data : numpy array
        The weighted input signal.

    """
    return data * halfsin(len(data))
