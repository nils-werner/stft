import urllib
import setuptools
import setuptools.command.develop


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
        'dspy'
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
        'develop': DevelopCommandProxy
    },
    zip_safe=False)
