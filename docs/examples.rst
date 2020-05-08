Examples
========

Simple Example
--------------

Loading a file and calculating the spectrogram.

.. code:: python

    import stft
    import scipy.io.wavfile as wav

    fs, audio = wav.read('input.wav')
    specgram = stft.spectrogram(audio)

.. seealso:: module :func:`stft.spectrogram`

Back and Forth Example
----------------------

Loading a file and calculating the spectrogram, its inverse and saving the
result.

.. code:: python

    import stft
    import scipy.io.wavfile as wav

    fs, audio = wav.read('input.wav')
    specgram = stft.spectrogram(audio)
    output = stft.ispectrogram(specgram)
    wav.write('output.wav', fs, output)

.. seealso:: modules :func:`stft.spectrogram` :func:`stft.ispectrogram`

Passing multiple transfer functions
-----------------------------------

:func:`stft.spectrogram` and :func:`stft.ispectrogram` allow passing multiple
transform functions as a list.

STFT will pick each transform for each frame it processes, the list of
transforms will be extended indefinitely for as long as many frames need to
be processed.

.. code:: python

    import stft
    import scipy.io.wavfile as wav

    fs, audio = wav.read('input.wav')
    specgram = stft.spectrogram(audio, transform=[scipy.fft.fft, numpy.fft.fft])
    output = stft.ispectrogram(specgram, transform=[scipy.fft.ifft, numpy.fft.ifft])
    wav.write('output.wav', fs, output)

In this case, each frame will be processed using :code:`scipy.fft.fft`,
then :code:`numpy.fft.fft`, then :code:`scipy.fft.fft` again etc.

Saving Settings Example
-----------------------

You do not need to pass the same settings to :func:`stft.spectrogram` and
:func:`stft.ispectrogram` twice as the settings are saved in the array itself.

.. code:: python

    import stft
    import scipy.io.wavfile as wav

    fs, audio = wav.read('input.wav')
    specgram = stft.spectrogram(audio, framelength=512, overlap=4)
    output = stft.ispectrogram(specgram)
    wav.write('output.wav', fs, output)

.. seealso:: modules :func:`stft.spectrogram` :func:`stft.ispectrogram` :class:`stft.types.SpectogramArray`
