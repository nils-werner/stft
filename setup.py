from setuptools import setup

setup(
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
    packages=find_packages(),

    # Dependencies, this installs the entire Python scientific
    # computations stack
    install_requires=['nose>=1.3.0',
                      'numpy>=1.9',
                      'scipy>=0.14.0',
                      'ipython>=2.0',
                      'matplotlib>=1.4',
                      'PyAudio>=0.2.7',
                      'dspy'],

    # Link to dependencies that are not on PyPI, in this case
    # dspy
    dependency_links=["git+https://github.com/nils-werner/dspy.git#egg=dspy"],
    zip_safe=False)
