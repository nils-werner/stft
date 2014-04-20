import sys
import numpy
import os
import sphinx
import sphinx.apidoc
import urllib
import warnings
import setuptools
import setuptools.command.develop


class SphinxCommandProxy(setuptools.Command):
    user_options = []
    description = 'sphinx'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # metadata contains information supplied in setup()
        metadata = self.distribution.metadata
        src_dir = (self.distribution.package_dir or {'': ''})['']
        src_dir = os.path.join(os.getcwd(),  src_dir)

        # Build docs from docstrings in *.py files
        sphinx.apidoc.main(
            ['',
             '-o', os.path.join('docs', 'source','api'), src_dir])

        # Build the doc sources
        sphinx.main(['', '-c', 'docs',
                     '-D', 'project=' + metadata.name,
                     '-D', 'version=' + metadata.version,
                     '-D', 'release=' + metadata.version,
                     os.path.join('docs', 'source'),
                     os.path.join('docs', 'build')])


class DevelopCommandProxy(setuptools.command.develop.develop):
    """
    `develop` command
    """

    def run(self):
        # Download or generate any data that is not part of this
        # repository but is required for development:

        # urllib.urlretrieve(
        #     "http://work.audiolabs.uni-erlangen.de/project/input.wav",
        #     "data/input.wav"
        # )
        # urllib.urlretrieve(
        #     "http://work.audiolabs.uni-erlangen.de/project/input2.wav",
        #     "data/input2.wav"
        # )
        setuptools.command.develop.develop.run(self)

# See if we can use Cython
USE_CYTHON = False

if "--no-cython" not in sys.argv:
    try:
        from Cython.Distutils import build_ext
        from Cython.Build import cythonize
        USE_CYTHON = True
    except ImportError as e:
        warnings.warn(e.message)
else:
    sys.argv.remove("--no-cython")

ext = '.pyx' if USE_CYTHON else '.c'

extension = [
    setuptools.Extension("project.cython",
                         ["project/cython" + ext],
                         include_dirs=[numpy.get_include()]),
]

if USE_CYTHON:
    extension = cythonize(extension)

setuptools.setup(
    # Name of the project
    name='skeleton',

    # Version
    version='0.1',

    # Description
    description='A skeleton for scientific Python projects.',

    # Your contact information
    author='Nils Werner',
    author_email='nils.werner@gmail.com',

    # License
    license='commercial',

    # Packages in this project
    # find_packages() finds all these automatically for you
    packages=setuptools.find_packages(),

    # Dependencies, this installs the entire Python scientific
    # computations stack
    install_requires=[
        'nose>=1.3.0',
        'numpy>=1.8',
        'scipy>=0.13.0',
        'matplotlib>=1.3.1',
        'PyAudio>=0.2.7',
        'ipdb',
        'dspy',
        'sphinx',
        'sphinx_rtd_theme'
    ],

    tests_require=[
        'nose>=1.3.0'
    ],
    test_suite="nose.collector",

    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: Science/Research',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis'
    ],

    # Link to dependencies that are not on PyPI, in this case
    # dspy
    dependency_links=[
        'git+https://github.com/nils-werner/dspy.git#egg=dspy'
    ],

    # Register custom commands
    cmdclass={
        'develop': DevelopCommandProxy,
        'build_sphinx': SphinxCommandProxy
    },
    zip_safe=False,
    ext_modules=extension
)
