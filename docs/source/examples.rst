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

.. seealso:: module :py:mod:`stft.spectrogram`

Scene Example
-------------

Loading a file and calculating the spectrogram, its inverse and saving the
result.

.. code:: python

    import skadt
    import scipy.io.wavfile as wav
    
    fs, audio = wav.read('input.wav')
    specgram = stft.spectrogram(audio)
    output = stft.ispectrogram(specgram)
    wav.write('input-anchor.wav', fs, output)

.. seealso:: modules :py:mod:`stft.spectrogram` :py:mod:`stft.ispectrogram`
