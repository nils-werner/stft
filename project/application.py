#!/usr/bin/env python

# Import Python 3 behaviour into Python 2

# print("hello") instead of print "hello"
from __future__ import print_function

# all strings are unicode by default
from __future__ import unicode_literals

# from . import foo
from __future__ import absolute_import

# 1 / 2 == 0.5 and 1 // 2 == 0
from __future__ import division

import sys
import argparse
import scipy
import numpy


def main(argv=[]):
    parser = argparse.ArgumentParser(
        description='Main Program.'
    )
    parser.add_argument(
        '--opt',
        metavar="VAL", default=60, type=int,
        help="Some optional value of type integer, defaulting to 60."
    )

    args = parser.parse_args(argv)

    return numpy.zeros(100)


if __name__ == "__main__":
    main(sys.argv[1:])
