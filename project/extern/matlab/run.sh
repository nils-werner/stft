#!/usr/bin/env bash

# Save script and local directory to variables
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CWD="$(pwd)"

# Test if MATLAB works (licensing etc...)
if [ matlab -nodisplay -nosplash -r "quit" > /dev/null 2>&1 == 0 ]; then
    # Change to directory where script resides
    cd $DIR
    matlab -nodisplay -nosplash -r "main('$CWD/input.wav', '$CWD/output.mat'); quit" > /dev/null 2>&1

    # Change back to working directory
    cd $CWD

    # Convert MATLAB .mat file to numpy file
    $DIR/convert.py -- ./output.mat ./output.npy
    rm -- ./output.mat
fi
