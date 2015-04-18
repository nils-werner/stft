import numpy


class SpectrogramArray(numpy.ndarray):
    """NumpyArray with additional :code:`stft_settings` attribute for saving
    stft-specific settings.

    """
    def __new__(cls, input_array, stft_settings=None):
        obj = numpy.asarray(input_array).view(cls)
        obj.stft_settings = stft_settings
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.stft_settings = getattr(obj, 'stft_settings', None)
