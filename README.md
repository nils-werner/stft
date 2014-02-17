Skeleton
========

A skeleton for scientific Python projects.

Purpose
-------

Getting started with a new language can be tricky. There are many tools and
workflows that need to be learned in order to be able to fully utilize the
language.

Secondly, to make new projects useful to other people, a certain project layout
style should be followed as closely as possible.

This skeleton is there to help create a new project using the Python and SciPy
software stack. It uses popular tools to install and separate single projects
and their dependencies from other projects.

Installation
------------

create a new virtual environment `<name>` and activate it:

    virtualenv --system-site-packages NAME
    cd NAME
    source bin/activate

copy/clone the source files there:

    git clone git@work.audiolabs.uni-erlangen.de:nils/python-skeleton.git
    cd python-skeleton

install the software and its dependencies:

    python setup.py install


Structure
---------

Your program should be structured as follows:

 - `project/`: Source code, change `project` to reflect your project name
  - `project/extern/`: All external code, e.g. MATLAB and C  
    Example scripts for interacting with matlab and converting .mat to .npy  
    files back and forth are provided there.  
 - `doc/`: Project documentation
 - `tests/`: Unit tests
 - `setup.py`: Installation script

Dependencies
------------

Python dependencies should be managed in the `setup.py` file. They will
automatically be installed when running `python setup.py install`.

Other language dependencies should go in `src/extern/`.

References
----------

 - [Sample Project][1] by the Python Package Authority

 [1]: https://github.com/pypa/sampleproject