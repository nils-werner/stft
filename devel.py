import stft
import numpy
import scipy.fftpack
import matplotlib.pyplot as plt

framelen = 512
a = numpy.random.random(2048)

x = stft.spectrogram(a, framelength=framelen)
y = stft.ispectrogram(x, framelength=framelen)

print x.shape, y.shape

plt.plot(a-y)
plt.show()
