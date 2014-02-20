#!/usr/bin/env python

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
