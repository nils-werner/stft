def test_main():
    import numpy
    from project import main

    # Make sure main returns an array
    assert type(main()) == numpy.ndarray