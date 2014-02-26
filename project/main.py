#!/usr/bin/env python

# Import Python 3 behaviour into Python 2
from __future__ import print_function           # print("hello") instead of print "hello"
from __future__ import unicode_literals         # all strings are unicode by default
from __future__ import absolute_import          # from . import foo
from __future__ import division                 # 1 / 2 == 0.5 and 1 // 2 == 0

import sys, os
import argparse
import scipy, numpy

def main(argv):
    parser = argparse.ArgumentParser(description='Main Program.')
    parser.add_argument('--opt', metavar="VAL", default=60, type=int, help="Optional value of some sort.")
    args = parser.parse_args(argv)

    return numpy.zeros(100)

if __name__ == "__main__":
    main(sys.argv[1:])
