from __future__ import division
import numpy
import math


def pad(data, framelength):
    return numpy.lib.pad(
        data,
        pad_width=(
            0,
            int(
                math.ceil(
                    len(data) / framelength
                ) * framelength - len(data)
            )
        ),
        mode='constant',
        constant_values=0
    )


def unpad(data, outlength):
    slicetuple = [slice(None)] * data.ndim
    slicetuple[0] = slice(None, outlength)
    return data[slicetuple]


def center_pad(data, framelength):
    padtuple = [(0, 0)] * data.ndim
    padtuple[0] = (framelength // 2, framelength // 2)
    return numpy.lib.pad(
        data,
        pad_width=padtuple,
        mode='constant',
        constant_values=0
    )


def center_unpad(data, framelength):
    padtuple = [(0, 0)] * data.ndim
    padtuple[0] = (framelength // 2, framelength // 2)
    return numpy.lib.pad(
        data,
        pad_width=padtuple,
        mode='constant',
        constant_values=0
    )


def center_unpad(data, framelength):
    slicetuple = [slice(None)] * data.ndim
    slicetuple[0] = slice(framelength // 2, -framelength // 2)
    return data[slicetuple]
