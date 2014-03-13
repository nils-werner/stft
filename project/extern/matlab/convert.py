#!/usr/bin/env python2

import os
import sys
import argparse
import numpy
import scipy.io


def main(argv):
    parser = argparse.ArgumentParser(
        description='Convert NumPy to Matlab data files and vice versa.'
    )
    parser.add_argument(
        'infile',
        help='Input file, either Numpy .npy or MATLAB .mat format.'
    )
    parser.add_argument(
        'outfile',
        help='Output file to be created, either Numpy .npy or MATLAB .mat format.'
    )
    args = parser.parse_args(argv)

    # Convert Numpy to MATLAB
    if os.path.splitext(args.infile)[1] == ".npy":
        scipy.io.savemat(args.outfile, {'array': numpy.load(args.infile)})

    # Convert MATLAB to Numpy
    elif os.path.splitext(args.infile)[1] == ".mat":
        numpy.save(args.outfile, scipy.io.loadmat(args.infile))

if __name__ == "__main__":
    main(sys.argv[1:])
