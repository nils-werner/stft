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
