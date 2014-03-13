def test_main():
    import numpy
    from project import application

    # Make sure main returns an array
    assert type(application.main()) == numpy.ndarray
